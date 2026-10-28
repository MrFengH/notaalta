from django.contrib import messages
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.cart.cart import Cart
from apps.catalog.models import Product

from .forms import CheckoutForm
from .models import SHIPPING_DETAILS, Order, OrderItem, PaymentMethod, ShippingMethod, shipping_cost


def _initial_from_user(user):
    if not user.is_authenticated:
        return {}
    initial = {"full_name": user.get_full_name(), "email": user.email}
    profile = getattr(user, "profile", None)
    if profile:
        for field in ("phone", "province", "district", "address", "reference"):
            initial[field] = getattr(profile, field)
    return initial


def _shipping_options(subtotal):
    return [
        {
            "value": method.value,
            "label": method.label,
            "eta": SHIPPING_DETAILS[method]["eta"],
            "cost": shipping_cost(method, subtotal),
            "free_from": SHIPPING_DETAILS[method]["free_from"],
        }
        for method in ShippingMethod
    ]


PAYMENT_HINTS = {
    PaymentMethod.TARJETA: "Visa o Mastercard. Pago simulado en esta demo.",
    PaymentMethod.YAPPY: "Recibirás la solicitud de pago en tu app Yappy.",
    PaymentMethod.ACH: "Te enviamos los datos de la cuenta por correo.",
    PaymentMethod.CONTRA_ENTREGA: "Efectivo o tarjeta al recibir. Solo Ciudad de Panamá.",
}


def checkout(request):
    cart = Cart(request)
    if not cart.lines:
        messages.info(request, "Tu carrito está vacío. Agrega un perfume para continuar.")
        return redirect("cart:detail")

    form = CheckoutForm(request.POST or None, initial=_initial_from_user(request.user))
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            products = Product.objects.select_for_update().in_bulk([l.product.pk for l in cart.lines])
            short = [l for l in cart.lines if products[l.product.pk].stock < l.quantity]
            if short:
                for line in short:
                    cart.set(line.product, products[line.product.pk].stock)
                messages.error(request, "Algunos productos cambiaron de disponibilidad. Ajustamos las cantidades; revisa tu carrito.")
                return redirect("cart:detail")

            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.subtotal = cart.subtotal
            order.discount = cart.discount
            order.coupon_code = cart.coupon.code if cart.discount else ""
            order.shipping_cost = shipping_cost(order.shipping_method, cart.total)
            order.total = cart.total + order.shipping_cost
            if order.payment_method in (PaymentMethod.TARJETA, PaymentMethod.YAPPY):
                order.status = Order.Status.PAGADO  # pago simulado aprobado
            order.save()
            for line in cart.lines:
                OrderItem.objects.create(
                    order=order, product=line.product, product_name=str(line.product),
                    unit_price=line.unit_price, quantity=line.quantity,
                )
                product = products[line.product.pk]
                product.stock -= line.quantity
                product.save(update_fields=["stock"])

        if request.user.is_authenticated and hasattr(request.user, "profile"):
            profile = request.user.profile
            if not profile.address:
                for field in ("phone", "province", "district", "address", "reference"):
                    setattr(profile, field, form.cleaned_data[field])
                profile.save()
        cart.clear()
        request.session["last_order_id"] = order.pk
        return redirect("orders:confirmation", order_id=order.pk)

    shipping_value = form["shipping_method"].value() or ShippingMethod.CIUDAD
    payment_value = form["payment_method"].value() or PaymentMethod.TARJETA
    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart": cart,
            "shipping_options": _shipping_options(cart.total),
            "shipping_value": shipping_value,
            "payment_options": [
                {"value": m.value, "label": m.label, "hint": PAYMENT_HINTS[m]} for m in PaymentMethod
            ],
            "payment_value": payment_value,
            "initial_shipping_cost": shipping_cost(shipping_value, cart.total),
            "initial_total": cart.total + shipping_cost(shipping_value, cart.total),
        },
    )


def confirmation(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id)
    allowed = request.session.get("last_order_id") == order.pk or (
        request.user.is_authenticated and order.user_id == request.user.pk
    )
    if not allowed:
        raise Http404
    return render(request, "orders/confirmation.html", {"order": order})
