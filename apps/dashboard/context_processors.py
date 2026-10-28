DASH_NAV = [
    ("overview", "Resumen", "ph-squares-four", "dashboard:overview"),
    ("orders", "Pedidos", "ph-receipt", "dashboard:orders"),
    ("customers", "Clientes", "ph-users", "dashboard:customers"),
    ("products", "Productos", "ph-flask", "dashboard:products"),
    ("inventory", "Inventario", "ph-stack", "dashboard:inventory"),
    ("brands", "Marcas", "ph-bookmark-simple", "dashboard:brands"),
]


def dashboard(request):
    if request.path.startswith("/panel/"):
        return {"dash_nav": DASH_NAV}
    return {}
