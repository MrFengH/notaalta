from datetime import timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Count, F, Max, Q, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.catalog.models import Brand, Category, Product
from apps.orders.forms import OrderStatusForm
from apps.orders.models import Order, OrderItem

from .forms import BrandForm, ProductForm, StockForm

User = get_user_model()
staff = staff_member_required(login_url="accounts:login")
VALID = ~Q(status=Order.Status.CANCELADO)


def _page(request, qs, size=20):
    page = Paginator(qs, size).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return page, params.urlencode()


@staff
def overview(request):
    now = timezone.localtime()
    valid = Order.objects.filter(VALID)
    totals = valid.aggregate(revenue=Sum("total"), count=Count("id"))
    revenue = totals["revenue"] or Decimal("0")
    count = totals["count"] or 0

    since = (now - timedelta(days=29)).date()
    by_day = dict(
        valid.filter(created_at__date__gte=since)
        .annotate(day=TruncDate("created_at", tzinfo=now.tzinfo))
        .values_list("day")
        .annotate(t=Sum("total"))
    )
    days = [since + timedelta(days=i) for i in range(30)]
    series = [{"day": d, "total": by_day.get(d, Decimal("0"))} for d in days]
    peak = max((s["total"] for s in series), default=0) or 1
    for s in series:
        s["pct"] = round(float(s["total"]) / float(peak) * 100, 1)
    last30 = sum(s["total"] for s in series)
    prev30 = valid.filter(
        created_at__date__gte=since - timedelta(days=30), created_at__date__lt=since
    ).aggregate(t=Sum("total"))["t"] or Decimal("0")

    status_counts = dict(Order.objects.values_list("status").annotate(n=Count("id")))
    statuses = [
        {"value": s.value, "label": s.label, "count": status_counts.get(s.value, 0)} for s in Order.Status
    ]
    top_products = (
        OrderItem.objects.filter(order__in=valid)
        .values("product_name")
        .annotate(units=Sum("quantity"), revenue=Sum(F("quantity") * F("unit_price")))
        .order_by("-units")[:5]
    )
    return render(
        request,
        "dashboard/overview.html",
        {
            "section": "overview",
            "revenue": revenue,
            "order_count": count,
            "avg_ticket": (revenue / count) if count else 0,
            "customer_count": User.objects.filter(is_staff=False).count(),
            "to_fulfil": Order.objects.filter(status__in=[Order.Status.PAGADO, Order.Status.PREPARANDO]).count(),
            "pending_payment": status_counts.get(Order.Status.PENDIENTE, 0),
            "series": series,
            "peak": peak,
            "last30": last30,
            "prev30": prev30,
            "trend": ((last30 - prev30) / prev30 * 100) if prev30 else None,
            "statuses": statuses,
            "recent": Order.objects.select_related("user")[:6],
            "low_stock_count": Product.objects.filter(stock__lte=Product.LOW_STOCK).count(),
            "low_stock": Product.objects.filter(stock__lte=Product.LOW_STOCK).select_related("brand").order_by("stock")[:6],
            "top_products": top_products,
        },
    )


@staff
def order_list(request):
    qs = Order.objects.select_related("user").annotate(units=Sum("items__quantity")).order_by("-created_at")
    status = request.GET.get("estado", "")
    q = request.GET.get("q", "").strip()
    if status in Order.Status.values:
        qs = qs.filter(status=status)
    if q:
        number = q.upper().removeprefix("NA-").lstrip("0")
        cond = Q(full_name__icontains=q) | Q(email__icontains=q)
        if number.isdigit():
            cond |= Q(pk=int(number))
        qs = qs.filter(cond)
    page, querystring = _page(request, qs)
    counts = dict(Order.objects.values_list("status").annotate(n=Count("id")))
    tabs = [{"value": "", "label": "Todos", "count": sum(counts.values())}] + [
        {"value": s.value, "label": s.label, "count": counts.get(s.value, 0)} for s in Order.Status
    ]
    return render(
        request,
        "dashboard/orders.html",
        {"section": "orders", "page_obj": page, "querystring": querystring, "tabs": tabs, "status": status, "q": q},
    )


@staff
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related("user").prefetch_related("items__product"), pk=pk)
    form = OrderStatusForm(request.POST or None, instance=order)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Pedido {order.number} actualizado: {order.get_status_display()}.")
        return redirect("dashboard:order", pk=order.pk)
    return render(request, "dashboard/order_detail.html", {"section": "orders", "order": order, "form": form})


@staff
def customer_list(request):
    qs = User.objects.filter(is_staff=False).select_related("profile").annotate(
        order_count=Count("orders", filter=~Q(orders__status=Order.Status.CANCELADO)),
        spent=Sum("orders__total", filter=~Q(orders__status=Order.Status.CANCELADO)),
        last_order=Max("orders__created_at"),
    )
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q))
    sort = request.GET.get("orden", "gasto")
    qs = qs.order_by({"gasto": F("spent").desc(nulls_last=True), "reciente": F("last_order").desc(nulls_last=True),
                      "nombre": F("first_name").asc()}.get(sort, F("spent").desc(nulls_last=True)))
    page, querystring = _page(request, qs)
    return render(
        request,
        "dashboard/customers.html",
        {"section": "customers", "page_obj": page, "querystring": querystring, "q": q, "sort": sort},
    )


@staff
def customer_detail(request, pk):
    customer = get_object_or_404(User.objects.select_related("profile"), pk=pk, is_staff=False)
    orders = customer.orders.annotate(units=Sum("items__quantity")).order_by("-created_at")
    stats = orders.filter(VALID).aggregate(spent=Sum("total"), n=Count("id"))
    return render(
        request,
        "dashboard/customer_detail.html",
        {
            "section": "customers",
            "customer": customer,
            "orders": orders,
            "spent": stats["spent"] or 0,
            "order_count": stats["n"],
            "avg": (stats["spent"] / stats["n"]) if stats["n"] else 0,
        },
    )


def _product_filter(request):
    qs = Product.objects.select_related("brand", "category")
    q = request.GET.get("q", "").strip()
    brand = request.GET.get("marca", "")
    category = request.GET.get("categoria", "")
    stock = request.GET.get("stock", "")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(brand__name__icontains=q))
    if brand:
        qs = qs.filter(brand__slug=brand)
    if category:
        qs = qs.filter(category__slug=category)
    if stock == "bajo":
        qs = qs.filter(stock__gt=0, stock__lte=Product.LOW_STOCK)
    elif stock == "agotado":
        qs = qs.filter(stock=0)
    filters = {"q": q, "brand": brand, "category": category, "stock": stock}
    return qs, filters


@staff
def product_list(request):
    qs, filters = _product_filter(request)
    page, querystring = _page(request, qs.order_by("brand__name", "name"))
    return render(
        request,
        "dashboard/products.html",
        {
            "section": "products", "page_obj": page, "querystring": querystring, "filters": filters,
            "brands": Brand.objects.all(), "categories": Category.objects.all(),
        },
    )


@staff
def product_form(request, pk=None):
    product = get_object_or_404(Product, pk=pk) if pk else None
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        messages.success(request, f"{'Actualizamos' if product else 'Creamos'} «{saved}».")
        return redirect("dashboard:products")
    return render(request, "dashboard/product_form.html", {"section": "products", "form": form, "product": product})


@staff
def inventory(request):
    qs, filters = _product_filter(request)
    qs = qs.order_by("stock", "brand__name")
    page, querystring = _page(request, qs, size=30)
    summary = Product.objects.aggregate(
        units=Sum("stock"),
        value=Sum(F("stock") * F("price")),
        out=Count("id", filter=Q(stock=0)),
        low=Count("id", filter=Q(stock__gt=0, stock__lte=Product.LOW_STOCK)),
    )
    return render(
        request,
        "dashboard/inventory.html",
        {
            "section": "inventory", "page_obj": page, "querystring": querystring, "filters": filters,
            "summary": summary, "categories": Category.objects.all(), "brands": Brand.objects.all(),
        },
    )


@staff
@require_POST
def inventory_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = StockForm(request.POST)
    if form.is_valid():
        product.stock = form.cleaned_data["stock"]
        product.save(update_fields=["stock", "updated_at"])
        messages.success(request, f"Inventario de {product}: {product.stock} unidades.")
    else:
        messages.error(request, f"El inventario de {product} debe ser un número entero entre 0 y 9999.")
    back = request.POST.get("back", "")
    return redirect(reverse("dashboard:inventory") + (f"?{back}" if back else ""))


@staff
def brand_list(request):
    brands = list(Brand.objects.annotate(product_count=Count("products"), stock=Sum("products__stock")).order_by("name"))
    sold = dict(
        OrderItem.objects.filter(order__in=Order.objects.filter(VALID))
        .values_list("product__brand_id")
        .annotate(units=Sum("quantity"))
    )
    for b in brands:
        b.units_sold = sold.get(b.pk, 0)
    return render(request, "dashboard/brands.html", {"section": "brands", "brands": brands})


@staff
def brand_form(request, pk=None):
    brand = get_object_or_404(Brand, pk=pk) if pk else None
    form = BrandForm(request.POST or None, instance=brand)
    if request.method == "POST" and form.is_valid():
        saved = form.save()
        messages.success(request, f"{'Actualizamos' if brand else 'Creamos'} la marca {saved}.")
        return redirect("dashboard:brands")
    return render(request, "dashboard/brand_form.html", {"section": "brands", "form": form, "brand": brand})
