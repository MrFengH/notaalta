from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_detail, name="detail"),
    path("agregar/<int:product_id>/", views.cart_add, name="add"),
    path("actualizar/<int:product_id>/", views.cart_update, name="update"),
    path("quitar/<int:product_id>/", views.cart_remove, name="remove"),
    path("cupon/", views.cart_coupon, name="coupon"),
]
