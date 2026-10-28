from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.catalog.models import Coupon, Product

from .cart import Cart


def _wants_json(request):
    return request.headers.get("x-requested-with") == "fetch"


def _qty(request, default=1):
    try:
        return max(int(request.POST.get("quantity", default)), 0)
    except (TypeError, ValueError):
        return default


def cart_detail(request):
    cart = Cart(request)
    free_from = Decimal(settings.STORE["free_shipping_from"])
    return render(request, "cart/detail.html", {"cart": cart, "free_remaining": max(free_from - cart.total, 0)})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product.objects.active(), pk=product_id)
    cart = Cart(request)
    if not product.in_stock:
        msg, ok = f"{product.name} está agotado por ahora.", False
    else:
        before = cart.data["items"].get(str(product.pk), 0)
        cart.add(product, _qty(request))
        after = cart.data["items"].get(str(product.pk), 0)
        if after == before:
            msg, ok = f"Ya tienes todas las unidades disponibles de {product.name}.", False
        else:
            msg, ok = f"{product.name} se agregó al carrito.", True
    if _wants_json(request):
        return JsonResponse({"ok": ok, "message": msg, "count": cart.count})
    (messages.success if ok else messages.warning)(request, msg)
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart(request)
    qty = _qty(request)
    cart.set(product, qty)
    if qty > product.stock:
        messages.warning(request, f"Solo quedan {product.stock} unidades de {product.name}.")
    return redirect("cart:detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    product = Product.objects.filter(pk=product_id).first()
    if product:
        messages.info(request, f"Quitamos {product.name} del carrito.")
    return redirect("cart:detail")


@require_POST
def cart_coupon(request):
    cart = Cart(request)
    if request.POST.get("remove"):
        cart.set_coupon("")
        messages.info(request, "Quitamos el cupón.")
        return redirect("cart:detail")
    code = request.POST.get("code", "").strip()
    coupon = Coupon.objects.filter(code__iexact=code, is_active=True).first()
    if not code:
        messages.error(request, "Escribe un código de cupón.")
    elif not coupon:
        messages.error(request, f"El cupón “{code}” no existe o ya venció. Revisa que esté bien escrito.")
    else:
        cart.set_coupon(coupon.code)
        if cart.discount:
            messages.success(request, f"Cupón {coupon.code} aplicado: {coupon.percent_off}% de descuento.")
        else:
            messages.warning(
                request,
                f"Cupón {coupon.code} guardado, pero no aplica a los productos de tu carrito"
                + (f" (solo {coupon.brand.name})." if coupon.brand else "."),
            )
    return redirect("cart:detail")
