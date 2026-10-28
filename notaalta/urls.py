from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.catalog.urls")),
    path("carrito/", include("apps.cart.urls")),
    path("checkout/", include("apps.orders.urls")),
    path("cuenta/", include("apps.accounts.urls")),
    path("panel/", include("apps.dashboard.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Nota Alta · Administración Django"
