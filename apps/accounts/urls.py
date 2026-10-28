from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.profile, name="profile"),
    path("ingresar/", views.StoreLoginView.as_view(), name="login"),
    path("salir/", views.StoreLogoutView.as_view(), name="logout"),
    path("registro/", views.register, name="register"),
    path("pedidos/<int:pk>/", views.order_detail, name="order"),
]
