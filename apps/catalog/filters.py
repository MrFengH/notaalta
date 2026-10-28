"""Filtros del catálogo leídos desde la query string (GET), sin estado en servidor."""

from decimal import Decimal, InvalidOperation

from django.db.models import Count, F, Q

from .models import Brand, Product

SORTS = {
    "relevancia": ("Destacados", ["-is_featured", "-created_at"]),
    "precio_asc": ("Precio: menor a mayor", ["price"]),
    "precio_desc": ("Precio: mayor a menor", ["-price"]),
    "nuevos": ("Novedades", ["-created_at"]),
}

PRICE_PRESETS = [
    ("", "50", "Hasta $50"),
    ("50", "100", "$50 a $100"),
    ("100", "150", "$100 a $150"),
    ("150", "", "Más de $150"),
]


def _decimal(value):
    try:
        return Decimal(value) if value not in (None, "") else None
    except InvalidOperation:
        return None


class CatalogFilter:
    def __init__(self, params, base_qs):
        self.params = params
        self.base_qs = base_qs
        self.q = params.get("q", "").strip()
        self.brands = params.getlist("marca")
        self.families = params.getlist("familia")
        self.concentrations = params.getlist("concentracion")
        self.price_min = _decimal(params.get("precio_min"))
        self.price_max = _decimal(params.get("precio_max"))
        self.on_sale = params.get("oferta") == "1"
        self.available = params.get("disponible") == "1"
        self.sort = params.get("orden") if params.get("orden") in SORTS else "relevancia"

    def _search(self, qs):
        if not self.q:
            return qs
        terms = Q()
        for word in self.q.split():
            terms &= (
                Q(name__icontains=word) | Q(brand__name__icontains=word)
                | Q(short_description__icontains=word) | Q(notes_top__icontains=word)
                | Q(notes_heart__icontains=word) | Q(notes_base__icontains=word)
            )
        return qs.filter(terms)

    @property
    def queryset(self):
        qs = self._search(self.base_qs)
        if self.brands:
            qs = qs.filter(brand__slug__in=self.brands)
        if self.families:
            qs = qs.filter(family__in=self.families)
        if self.concentrations:
            qs = qs.filter(concentration__in=self.concentrations)
        if self.price_min is not None:
            qs = qs.filter(price__gte=self.price_min)
        if self.price_max is not None:
            qs = qs.filter(price__lte=self.price_max)
        if self.on_sale:
            qs = qs.filter(compare_at_price__gt=F("price"))
        if self.available:
            qs = qs.filter(stock__gt=0)
        return qs.order_by(*SORTS[self.sort][1])

    # -- facetas para el panel lateral ------------------------------------
    def brand_facets(self):
        scope = self._search(self.base_qs)
        counts = dict(scope.values_list("brand__slug").annotate(n=Count("id")))
        return [
            {"slug": b.slug, "name": b.name, "count": counts.get(b.slug, 0), "checked": b.slug in self.brands}
            for b in Brand.objects.filter(slug__in=counts)
        ]

    def family_facets(self):
        scope = self._search(self.base_qs)
        counts = dict(scope.values_list("family").annotate(n=Count("id")))
        return [
            {"value": v, "label": label, "count": counts[v], "checked": v in self.families}
            for v, label in Product.Family.choices if v in counts
        ]

    def concentration_facets(self):
        scope = self._search(self.base_qs)
        counts = dict(scope.values_list("concentration").annotate(n=Count("id")))
        return [
            {"value": v, "label": label, "count": counts[v], "checked": v in self.concentrations}
            for v, label in Product.Concentration.choices if v in counts
        ]

    def price_presets(self):
        current = (self.params.get("precio_min", ""), self.params.get("precio_max", ""))
        return [
            {"min": lo, "max": hi, "label": label, "checked": current == (lo, hi)}
            for lo, hi, label in PRICE_PRESETS
        ]

    def active_chips(self):
        """Filtros aplicados, cada uno con la URL que lo quita."""
        chips = []

        def without(key, value=None):
            params = self.params.copy()
            if value is None:
                params.pop(key, None)
            else:
                params.setlist(key, [v for v in params.getlist(key) if v != value])
            params.pop("page", None)
            return "?" + params.urlencode()

        brand_names = dict(Brand.objects.filter(slug__in=self.brands).values_list("slug", "name"))
        for slug in self.brands:
            chips.append({"label": brand_names.get(slug, slug), "url": without("marca", slug)})
        families = dict(Product.Family.choices)
        for f in self.families:
            chips.append({"label": families.get(f, f), "url": without("familia", f)})
        concentrations = dict(Product.Concentration.choices)
        for c in self.concentrations:
            chips.append({"label": concentrations.get(c, c), "url": without("concentracion", c)})
        if self.price_min is not None or self.price_max is not None:
            params = self.params.copy()
            params.pop("precio_min", None)
            params.pop("precio_max", None)
            lo = f"${self.price_min:g}" if self.price_min is not None else "$0"
            hi = f"${self.price_max:g}" if self.price_max is not None else "más"
            chips.append({"label": f"{lo} a {hi}", "url": "?" + params.urlencode()})
        if self.on_sale:
            chips.append({"label": "Con descuento", "url": without("oferta")})
        if self.available:
            chips.append({"label": "Disponible", "url": without("disponible")})
        return chips

    @property
    def active_count(self):
        return len(self.active_chips())

    @property
    def sort_options(self):
        return [(key, label) for key, (label, _) in SORTS.items()]
