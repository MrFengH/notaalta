from django.core.management import call_command
from django.test import TestCase

from apps.catalog.models import Brand, Category, Product

from .forms import BrandForm, ProductForm


class SlugAutoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_store", verbosity=0)

    def data(self, **kw):
        return {"name": "Coco Mademoiselle", "brand": Brand.objects.get(slug="chanel").pk,
                "category": Category.objects.get(slug="damas").pk, "family": "chipre", "concentration": "edp",
                "volume_ml": 100, "short_description": "x", "description": "y", "price": "10", "stock": 1, **kw}

    def test_empty_slug_is_generated_and_unique(self):
        form = ProductForm(data=self.data())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().slug, "chanel-coco-mademoiselle-100ml-2")
        self.assertNotIn("slug", form.fields)

    def test_editing_keeps_own_slug(self):
        product = Product.objects.get(slug="chanel-coco-mademoiselle-100ml")
        form = ProductForm(data=self.data(name="Otro nombre"), instance=product)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save().slug, "chanel-coco-mademoiselle-100ml")

    def test_brand_slug_strips_accents(self):
        form = BrandForm(data={"name": "Maison Ñandú", "slug": ""})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["slug"], "maison-nandu")
