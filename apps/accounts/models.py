from django.conf import settings
from django.db import models

from apps.orders.models import PROVINCES


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField("teléfono", max_length=30, blank=True)
    province = models.CharField("provincia", max_length=30, choices=PROVINCES, blank=True)
    district = models.CharField("distrito o corregimiento", max_length=80, blank=True)
    address = models.CharField("dirección", max_length=200, blank=True)
    reference = models.CharField("punto de referencia", max_length=200, blank=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self):
        return f"Perfil de {self.user}"
