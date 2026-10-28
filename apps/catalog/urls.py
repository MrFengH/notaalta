from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("tienda/", views.catalog, name="catalog"),
    path("categoria/<slug:slug>/", views.category, name="category"),
    path("marcas/", views.brands, name="brands"),
    path("marca/<slug:slug>/", views.brand, name="brand"),
    path("perfume/<slug:slug>/", views.product_detail, name="product"),
]
