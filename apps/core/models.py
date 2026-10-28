from django.db import models


class ContactMessage(models.Model):
    class Topic(models.TextChoices):
        PEDIDO = "pedido", "Un pedido"
        PRODUCTO = "producto", "Un producto"
        OTRO = "otro", "Otro tema"

    name = models.CharField("nombre", max_length=120)
    email = models.EmailField("correo")
    topic = models.CharField("tema", max_length=20, choices=Topic.choices, default=Topic.PRODUCTO)
    message = models.TextField("mensaje")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"

    def __str__(self):
        return f"{self.name} · {self.get_topic_display()}"
