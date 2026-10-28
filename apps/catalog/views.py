from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .filters import CatalogFilter
from .models import Brand, Category, Coupon, Product

PAGE_SIZE = 12


def brand_coupons():
    """Mapa brand_id -> cupón activo, para mostrarlo en las tarjetas."""
    return {c.brand_id: c for c in Coupon.objects.filter(is_active=True, brand__isnull=False)}


def _listing(request, base_qs, context):
    flt = CatalogFilter(request.GET, base_qs)
    paginator = Paginator(flt.queryset.select_related("brand", "category"), PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context.update(
        {
            "filter": flt,
            "page_obj": page,
            "products": page.object_list,
            "querystring": params.urlencode(),
            "coupons": brand_coupons(),
        }
    )
    return render(request, "catalog/list.html", context)


def catalog(request):
    q = request.GET.get("q", "").strip()
    title = f"Resultados para “{q}”" if q else "Todos los perfumes"
    return _listing(request, Product.objects.active(), {"title": title, "search_query": q})


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    return _listing(
        request,
        Product.objects.active().filter(category=cat),
        {"title": cat.name, "intro": cat.tagline, "category": cat},
    )


def brand(request, slug):
    br = get_object_or_404(Brand, slug=slug)
    return _listing(
        request,
        Product.objects.active().filter(brand=br),
        {"title": br.name, "intro": br.description, "brand": br, "hide_brand_filter": True},
    )


def brands(request):
    all_brands = Brand.objects.annotate(
        product_count=Count("products", filter=Q(products__is_active=True))
    ).filter(product_count__gt=0)
    featured = [b for b in all_brands if b.is_featured]
    groups = {}
    for b in all_brands:
        groups.setdefault(b.name[0].upper(), []).append(b)
    return render(
        request,
        "catalog/brands.html",
        {"featured": featured, "groups": sorted(groups.items()), "brand_total": len(all_brands)},
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.active().select_related("brand", "category").prefetch_related("gallery"), slug=slug
    )
    candidates = (
        Product.objects.active().filter(category=product.category).exclude(pk=product.pk).select_related("brand")
    )
    # Primero la misma familia olfativa, luego la misma marca, luego destacados
    related = sorted(
        candidates,
        key=lambda p: (p.family != product.family, p.brand_id != product.brand_id, not p.is_featured),
    )[:4]
    coupon = Coupon.objects.filter(is_active=True, brand=product.brand).first()
    images = [{"url": product.image_url, "alt": f"Frasco de {product}"}] + [
        {"url": g.image_url, "alt": g.alt or str(product)} for g in product.gallery.all()
    ]
    return render(
        request,
        "catalog/detail.html",
        {
            "product": product,
            "images": images,
            "related": related,
            "coupon": coupon,
            "coupons": brand_coupons(),
        },
    )
