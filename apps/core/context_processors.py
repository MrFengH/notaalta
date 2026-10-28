from django.conf import settings
from django.urls import reverse

from apps.catalog.models import Category

NAV = [
    ("Inicio", "core:home", None),
    ("Caballeros", "catalog:category", "caballeros"),
    ("Damas", "catalog:category", "damas"),
    ("Niños", "catalog:category", "ninos"),
    ("Marcas", "catalog:brands", None),
    ("Nosotros", "core:about", None),
    ("Contacto", "core:contact", None),
]


def store(request):
    path = request.path
    nav = []
    for label, name, arg in NAV:
        url = reverse(name, args=[arg] if arg else [])
        active = path == url if url == "/" else path.startswith(url)
        if name == "catalog:brands" and path.startswith("/marca/"):
            active = True
        nav.append({"label": label, "url": url, "active": active})
    return {"STORE": settings.STORE, "nav_links": nav, "nav_categories": Category.objects.all()}
