from decimal import ROUND_HALF_UP, Decimal

from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Category(models.Model):
    name = models.CharField("nombre", max_length=60)
    slug = models.SlugField(unique=True)
    tagline = models.CharField("frase corta", max_length=140, blank=True)
    image_static = models.CharField("imagen (ruta estática)", max_length=200, blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:category", args=[self.slug])


class Brand(models.Model):
    name = models.CharField("nombre", max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    country = models.CharField("país de origen", max_length=60, blank=True)
    description = models.TextField("descripción", blank=True)
    is_featured = models.BooleanField("destacada", default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "marca"
        verbose_name_plural = "marcas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:brand", args=[self.slug])


class Coupon(models.Model):
    code = models.CharField("código", max_length=30, unique=True)
    percent_off = models.PositiveSmallIntegerField("descuento (%)")
    brand = models.ForeignKey(
        Brand, verbose_name="solo para la marca", null=True, blank=True,
        on_delete=models.CASCADE, related_name="coupons",
    )
    description = models.CharField("descripción", max_length=140, blank=True)
    is_active = models.BooleanField("activo", default=True)

    class Meta:
        verbose_name = "cupón"
        verbose_name_plural = "cupones"

    def __str__(self):
        return self.code

    def applies_to(self, product):
        return self.brand_id is None or self.brand_id == product.brand_id


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def on_sale(self):
        return self.filter(compare_at_price__gt=models.F("price"))


class Product(models.Model):
    class Family(models.TextChoices):
        FLORAL = "floral", "Floral"
        CITRICA = "citrica", "Cítrica"
        AMADERADA = "amaderada", "Amaderada"
        ORIENTAL = "oriental", "Oriental"
        GOURMAND = "gourmand", "Gourmand"
        AROMATICA = "aromatica", "Aromática"
        ACUATICA = "acuatica", "Acuática"
        CHIPRE = "chipre", "Chipre"

    class Concentration(models.TextChoices):
        PARFUM = "parfum", "Parfum"
        EDP = "edp", "Eau de Parfum"
        EDT = "edt", "Eau de Toilette"
        EDC = "edc", "Eau de Cologne"
        MIST = "mist", "Bruma corporal"

    name = models.CharField("nombre", max_length=120)
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(Brand, verbose_name="marca", on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, verbose_name="categoría", on_delete=models.PROTECT, related_name="products")
    family = models.CharField("familia olfativa", max_length=20, choices=Family.choices)
    concentration = models.CharField("concentración", max_length=10, choices=Concentration.choices)
    volume_ml = models.PositiveSmallIntegerField("volumen (ml)")
    short_description = models.CharField("descripción corta", max_length=160)
    description = models.TextField("descripción")
    notes_top = models.CharField("notas de salida", max_length=160, blank=True)
    notes_heart = models.CharField("notas de corazón", max_length=160, blank=True)
    notes_base = models.CharField("notas de fondo", max_length=160, blank=True)
    price = models.DecimalField("precio", max_digits=8, decimal_places=2)
    compare_at_price = models.DecimalField(
        "precio anterior", max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Si es mayor que el precio, se muestra tachado como descuento.",
    )
    stock = models.PositiveIntegerField("inventario", default=0)
    image = models.ImageField("imagen", upload_to="products/", blank=True)
    image_static = models.CharField("imagen (ruta estática)", max_length=200, blank=True)
    is_featured = models.BooleanField("destacado", default=False)
    is_active = models.BooleanField("publicado", default=True)
    created_at = models.DateTimeField("creado", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado", auto_now=True)

    objects = ProductQuerySet.as_manager()

    LOW_STOCK = 5

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return f"{self.brand.name} {self.name}"

    def get_absolute_url(self):
        return reverse("catalog:product", args=[self.slug])

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.image_static:
            return static(self.image_static)
        return static("img/placeholder.webp")

    @property
    def on_sale(self):
        return bool(self.compare_at_price and self.compare_at_price > self.price)

    @property
    def discount_percent(self):
        if not self.on_sale:
            return 0
        pct = (1 - self.price / self.compare_at_price) * 100
        return int(Decimal(pct).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    @property
    def savings(self):
        return self.compare_at_price - self.price if self.on_sale else Decimal("0")

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def low_stock(self):
        return 0 < self.stock <= self.LOW_STOCK

    @property
    def spec_line(self):
        return f"{self.get_concentration_display()} · {self.volume_ml} ml"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField("imagen", upload_to="products/gallery/", blank=True)
    image_static = models.CharField("imagen (ruta estática)", max_length=200, blank=True)
    alt = models.CharField("texto alternativo", max_length=160, blank=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "imagen de galería"
        verbose_name_plural = "galería"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static(self.image_static)
