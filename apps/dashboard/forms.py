from django import forms
from django.utils.text import slugify

from apps.catalog.models import Brand, Product
from apps.core.forms import StyledFormMixin


def fill_slug(form, data, base):
    """Si el slug viene vacío, lo genera a partir de `base` y evita duplicados."""
    if data.get("slug") or not base.strip():
        return
    model = form._meta.model
    slug = root = slugify(base)[:45] or "item"
    n = 2
    while model.objects.filter(slug=slug).exclude(pk=form.instance.pk).exists():
        slug, n = f"{root}-{n}", n + 1
    data["slug"] = slug


SLUG_LABEL = "Dirección web (opcional)"


class ProductForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "brand", "category", "family", "concentration", "volume_ml",
            "short_description", "description", "notes_top", "notes_heart", "notes_base",
            "price", "compare_at_price", "stock", "image", "is_featured", "is_active",
        ]
        help_texts = {
            "short_description": "Una línea que aparece en la tarjeta del catálogo (máx. 160 caracteres).",
            "compare_at_price": "Déjalo vacío si el producto no tiene descuento.",
            "image": "JPG o WebP vertical (4:5), mínimo 800 × 1000 px.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0", "inputmode": "decimal"}),
            "compare_at_price": forms.NumberInput(attrs={"step": "0.01", "min": "0", "inputmode": "decimal"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["brand"].empty_label = "Selecciona una marca"
        self.fields["category"].empty_label = "Selecciona una categoría"
        self.fields["family"].choices = [("", "Selecciona una familia")] + list(self.fields["family"].choices)[1:]
        self.fields["concentration"].choices = [("", "Selecciona la concentración")] + list(self.fields["concentration"].choices)[1:]

    def clean(self):
        data = super().clean()
        if not self.instance.slug:  # al editar se conserva la URL existente
            brand, generated = data.get("brand"), {}
            fill_slug(self, generated, f"{brand.name if brand else ''} {data.get('name', '')} {data.get('volume_ml') or ''}ml")
            self.instance.slug = generated.get("slug", "")
        price, compare = data.get("price"), data.get("compare_at_price")
        if price is not None and compare is not None and compare <= price:
            self.add_error("compare_at_price", "El precio anterior debe ser mayor que el precio actual, o déjalo vacío.")
        return data


class BrandForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "slug", "country", "description", "is_featured"]
        labels = {"is_featured": "Mostrar en la página de inicio"}
        help_texts = {"slug": "Déjalo vacío y se genera solo con el nombre."}
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        self.fields["slug"].label = SLUG_LABEL

    def clean(self):
        data = super().clean()
        fill_slug(self, data, data.get("name", ""))
        return data


class StockForm(forms.Form):
    stock = forms.IntegerField(min_value=0, max_value=9999)
