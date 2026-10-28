from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.overview, name="overview"),
    path("pedidos/", views.order_list, name="orders"),
    path("pedidos/<int:pk>/", views.order_detail, name="order"),
    path("clientes/", views.customer_list, name="customers"),
    path("clientes/<int:pk>/", views.customer_detail, name="customer"),
    path("productos/", views.product_list, name="products"),
    path("productos/nuevo/", views.product_form, name="product_new"),
    path("productos/<int:pk>/", views.product_form, name="product_edit"),
    path("inventario/", views.inventory, name="inventory"),
    path("inventario/<int:pk>/", views.inventory_update, name="inventory_update"),
    path("marcas/", views.brand_list, name="brands"),
    path("marcas/nueva/", views.brand_form, name="brand_new"),
    path("marcas/<int:pk>/", views.brand_form, name="brand_edit"),
]
