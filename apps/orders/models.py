from decimal import Decimal

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.catalog.models import Product

PROVINCES = [
    ("panama", "Panamá"),
    ("panama-oeste", "Panamá Oeste"),
    ("colon", "Colón"),
    ("chiriqui", "Chiriquí"),
    ("cocle", "Coclé"),
    ("herrera", "Herrera"),
    ("los-santos", "Los Santos"),
    ("veraguas", "Veraguas"),
    ("bocas-del-toro", "Bocas del Toro"),
    ("darien", "Darién"),
    ("guna-yala", "Comarca Guna Yala"),
    ("ngabe-bugle", "Comarca Ngäbe-Buglé"),
    ("embera-wounaan", "Comarca Emberá-Wounaan"),
]


class ShippingMethod(models.TextChoices):
    CIUDAD = "ciudad", "Envío Ciudad de Panamá"
    INTERIOR = "interior", "Envío al interior"
    RETIRO = "retiro", "Retiro en tienda"


SHIPPING_DETAILS = {
    ShippingMethod.CIUDAD: {"cost": Decimal("4.50"), "eta": "24 a 48 horas", "free_from": Decimal("60")},
    ShippingMethod.INTERIOR: {"cost": Decimal("9.00"), "eta": "3 a 5 días hábiles", "free_from": None},
    ShippingMethod.RETIRO: {"cost": Decimal("0.00"), "eta": "Listo en 4 horas", "free_from": None},
}


def shipping_cost(method, subtotal):
    info = SHIPPING_DETAILS[ShippingMethod(method)]
    if info["free_from"] is not None and subtotal >= info["free_from"]:
        return Decimal("0.00")
    return info["cost"]


class PaymentMethod(models.TextChoices):
    TARJETA = "tarjeta", "Tarjeta de crédito o débito"
    YAPPY = "yappy", "Yappy"
    ACH = "ach", "Transferencia ACH"
    CONTRA_ENTREGA = "contra_entrega", "Pago contra entrega"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente de pago"
        PAGADO = "pagado", "Pagado"
        PREPARANDO = "preparando", "En preparación"
        ENVIADO = "enviado", "Enviado"
        ENTREGADO = "entregado", "Entregado"
        CANCELADO = "cancelado", "Cancelado"

    FLOW = [Status.PENDIENTE, Status.PAGADO, Status.PREPARANDO, Status.ENVIADO, Status.ENTREGADO]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="cliente", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="orders",
    )
    full_name = models.CharField("nombre completo", max_length=120)
    email = models.EmailField("correo")
    phone = models.CharField("teléfono", max_length=30)
    province = models.CharField("provincia", max_length=30, choices=PROVINCES)
    district = models.CharField("distrito o corregimiento", max_length=80)
    address = models.CharField("dirección", max_length=200)
    reference = models.CharField("punto de referencia", max_length=200, blank=True)
    shipping_method = models.CharField("envío", max_length=20, choices=ShippingMethod.choices)
    payment_method = models.CharField("pago", max_length=20, choices=PaymentMethod.choices)
    status = models.CharField("estado", max_length=20, choices=Status.choices, default=Status.PENDIENTE)
    coupon_code = models.CharField("cupón", max_length=30, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField("descuento", max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField("costo de envío", max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField("notas internas", blank=True)
    created_at = models.DateTimeField("fecha", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return self.number

    @property
    def number(self):
        return f"NA-{self.pk:05d}" if self.pk else "NA-nuevo"

    def get_absolute_url(self):
        return reverse("accounts:order", args=[self.pk])

    @property
    def item_count(self):
        return sum(i.quantity for i in self.items.all())

    @property
    def step_index(self):
        """Posición en el flujo para la línea de tiempo (-1 si está cancelado)."""
        if self.status == self.Status.CANCELADO:
            return -1
        return self.FLOW.index(self.status)

    def timeline(self):
        current = self.step_index
        return [
            {"label": status.label, "done": current >= i, "current": current == i}
            for i, status in enumerate(self.FLOW)
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name="order_items")
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "artículo"
        verbose_name_plural = "artículos"

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"

    @property
    def line_total(self):
        return self.unit_price * self.quantity
