from django.conf import settings


def cart(request):
    data = request.session.get(settings.CART_SESSION_KEY) or {}
    items = data.get("items", {}) if isinstance(data, dict) else {}
    return {"cart_count": sum(items.values())}
