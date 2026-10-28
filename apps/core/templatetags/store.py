from decimal import Decimal

from django import template

register = template.Library()

STATUS_TONES = {
    "pendiente": "warn",
    "pagado": "info",
    "preparando": "info",
    "enviado": "brand",
    "entregado": "success",
    "cancelado": "danger",
}


@register.filter
def money(value):
    """Formato de precio en dólares: $1,234.50"""
    try:
        value = Decimal(value or 0)
    except Exception:
        return value
    return f"${value:,.2f}"


@register.filter
def status_tone(status):
    return STATUS_TONES.get(status, "neutral")


@register.simple_tag(takes_context=True)
def query(context, **kwargs):
    """Devuelve la query string actual con los parámetros indicados reemplazados."""
    params = context["request"].GET.copy()
    for key, value in kwargs.items():
        if value in (None, ""):
            params.pop(key, None)
        else:
            params[key] = value
    if "page" not in kwargs:
        params.pop("page", None)
    return "?" + params.urlencode()


@register.filter
def lookup(mapping, key):
    return mapping.get(key) if mapping else None
