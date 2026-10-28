from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("confirmado/<int:order_id>/", views.confirmation, name="confirmation"),
]
