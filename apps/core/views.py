from django.contrib import messages
from django.shortcuts import redirect, render

from apps.catalog.models import Brand, Category, Coupon, Product
from apps.catalog.views import brand_coupons

from .forms import ContactForm

FAMILIES = [
    {"value": "citrica", "label": "Cítricos", "text": "Bergamota, limón y mandarina. Frescos para el calor.", "image": "img/editorial/citricos.webp"},
    {"value": "floral", "label": "Florales", "text": "Rosa, jazmín y flores blancas, de lo ligero a lo intenso.", "image": "img/products/narciso-for-her.webp"},
    {"value": "amaderada", "label": "Amaderados", "text": "Cedro, vetiver y sándalo. Elegantes y duraderos.", "image": "img/editorial/laboratorio.webp"},
    {"value": "gourmand", "label": "Gourmand", "text": "Vainilla, café y praliné para quien prefiere lo dulce.", "image": "img/products/prada-candy.webp"},
]


def home(request):
    products = Product.objects.active().select_related("brand")
    categories = {c.slug: c for c in Category.objects.all()}
    return render(
        request,
        "pages/home.html",
        {
            "bestsellers": products.filter(is_featured=True).exclude(category__slug="ninos").order_by("-price")[:8],
            "deals": products.on_sale().filter(stock__gt=0).exclude(category__slug="ninos").order_by("-compare_at_price")[:4],
            "categories": categories,
            "brands": Brand.objects.filter(is_featured=True)[:8],
            "promo": Coupon.objects.filter(is_active=True, brand__isnull=True).first(),
            "coupons": brand_coupons(),
            "families": FAMILIES,
        },
    )


def about(request):
    return render(request, "pages/about.html", {"brand_count": Brand.objects.count()})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Recibimos tu mensaje. Te respondemos por correo en menos de un día hábil.")
        return redirect("core:contact")
    return render(request, "pages/contact.html", {"form": form})
