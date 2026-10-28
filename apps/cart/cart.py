"""Carrito guardado en la sesión: {product_id: cantidad} más un cupón opcional."""

from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings

from apps.catalog.models import Coupon, Product

CENT = Decimal("0.01")


class CartLine:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def unit_price(self):
        return self.product.price

    @property
    def total(self):
        return self.product.price * self.quantity


class Cart:
    def __init__(self, request):
        self.session = request.session
        data = self.session.get(settings.CART_SESSION_KEY)
        if not isinstance(data, dict):
            data = {"items": {}, "coupon": ""}
        self.data = data
        self._lines = None

    # -- mutaciones -------------------------------------------------------
    def add(self, product, quantity=1):
        key = str(product.pk)
        current = self.data["items"].get(key, 0)
        self.data["items"][key] = min(current + quantity, product.stock)
        if self.data["items"][key] <= 0:
            self.data["items"].pop(key, None)
        self._save()

    def set(self, product, quantity):
        key = str(product.pk)
        quantity = min(max(quantity, 0), product.stock)
        if quantity:
            self.data["items"][key] = quantity
        else:
            self.data["items"].pop(key, None)
        self._save()

    def remove(self, product_id):
        self.data["items"].pop(str(product_id), None)
        self._save()

    def set_coupon(self, code):
        self.data["coupon"] = code
        self._save()

    def clear(self):
        self.session.pop(settings.CART_SESSION_KEY, None)
        self.session.modified = True
        self._lines = None

    def _save(self):
        self.session[settings.CART_SESSION_KEY] = self.data
        self.session.modified = True
        self._lines = None

    # -- lectura ----------------------------------------------------------
    @property
    def lines(self):
        if self._lines is None:
            ids = [int(k) for k in self.data["items"]]
            products = Product.objects.active().select_related("brand").in_bulk(ids)
            self._lines = [
                CartLine(products[int(k)], q)
                for k, q in self.data["items"].items()
                if int(k) in products
            ]
        return self._lines

    def __iter__(self):
        return iter(self.lines)

    def __len__(self):
        return sum(line.quantity for line in self.lines)

    @property
    def count(self):
        return sum(self.data["items"].values())

    @property
    def coupon(self):
        code = self.data.get("coupon")
        if not code:
            return None
        return Coupon.objects.filter(code__iexact=code, is_active=True).first()

    @property
    def subtotal(self):
        return sum((line.total for line in self.lines), Decimal("0.00"))

    @property
    def discount(self):
        coupon = self.coupon
        if not coupon:
            return Decimal("0.00")
        eligible = sum(
            (line.total for line in self.lines if coupon.applies_to(line.product)),
            Decimal("0.00"),
        )
        return (eligible * coupon.percent_off / 100).quantize(CENT, rounding=ROUND_HALF_UP)

    @property
    def total(self):
        return self.subtotal - self.discount
