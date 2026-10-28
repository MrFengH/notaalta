# Nota Alta · Perfumería online (Django)

Tienda de perfumes para Panamá: catálogo con filtros, ficha de producto, carrito, checkout simulado, perfil con historial de pedidos y un panel administrativo propio.

## Puesta en marcha

Requisitos: Python 3.11+ (Node.js solo si vas a cambiar estilos).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_store        # marcas, 23 perfumes, cupones, clientes y 62 pedidos de ejemplo
python manage.py runserver
```

Abre http://127.0.0.1:8000/

| Rol | Usuario | Contraseña |
|---|---|---|
| Cliente | cliente@notaalta.example | Cliente2026! |
| Administración (panel en /panel/) | admin@notaalta.example | NotaAlta2026! |

Cupones de prueba: `NOTA10` (10 % en todo), `DG10` (Dolce & Gabbana), `PETIT15` (línea infantil).

`python manage.py seed_store --reset` vuelve a cargar los datos de demostración.

## Estilos

El CSS compilado (`static/css/app.css`) ya está incluido. Para modificarlo:

```bash
npm install
npm run watch:css   # o npm run build:css
```

Los tokens de diseño y los componentes (`btn`, `input`, `badge`, `panel`, `data-table`, etc.) están en `static/src/app.css`.

## Estructura

```
notaalta/          configuración y URLs raíz
apps/
  core/            inicio, nosotros, contacto, context processors, filtros de plantilla, mixin de formularios
  catalog/         marcas, categorías, productos, galería, cupones, filtros del catálogo, comando seed_store
  cart/            carrito en sesión (con cupón) y endpoints (también vía fetch)
  orders/          pedidos, envío y pago, checkout y confirmación
  accounts/        registro, ingreso, perfil con dirección e historial de pedidos
  dashboard/       panel administrativo propio (/panel/)
templates/         plantillas por módulo + parciales reutilizables (tarjeta, campo, paginación, toasts)
static/            src/app.css (Tailwind v4), css/app.css (compilado), js/app.js, img/
```

## Notas

- Pagos y envíos son simulados: tarjeta y Yappy marcan el pedido como pagado; ACH y contra entrega quedan pendientes.
- Precios en USD con ITBMS incluido. Envío gratis en Ciudad de Panamá desde $60.
- Fotografías de Unsplash y Pexels (licencias libres). "Petit Atelier" es una marca ficticia de demostración; precios y pedidos son de ejemplo.
- Los iconos (Phosphor) y la tipografía (Schibsted Grotesk) se cargan desde CDN.
