from django import forms

from apps.core.forms import StyledFormMixin

from .models import Order, PaymentMethod, ShippingMethod


class CheckoutForm(StyledFormMixin, forms.ModelForm):
    shipping_method = forms.ChoiceField(
        label="Método de envío", choices=ShippingMethod.choices, widget=forms.RadioSelect,
        initial=ShippingMethod.CIUDAD,
    )
    payment_method = forms.ChoiceField(
        label="Método de pago", choices=PaymentMethod.choices, widget=forms.RadioSelect,
        initial=PaymentMethod.TARJETA,
    )

    class Meta:
        model = Order
        fields = [
            "full_name", "email", "phone",
            "province", "district", "address", "reference",
            "shipping_method", "payment_method",
        ]
        labels = {
            "full_name": "Nombre completo",
            "email": "Correo electrónico",
            "phone": "Teléfono celular",
            "province": "Provincia",
            "district": "Distrito o corregimiento",
            "address": "Dirección",
            "reference": "Punto de referencia (opcional)",
        }
        help_texts = {
            "email": "Te enviaremos la confirmación y el seguimiento del pedido.",
            "phone": "El repartidor te llamará a este número.",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel", "placeholder": "6123-4567"}),
            "district": forms.TextInput(attrs={"autocomplete": "address-level2", "placeholder": "Ej.: San Francisco"}),
            "address": forms.TextInput(attrs={"autocomplete": "street-address", "placeholder": "Calle, edificio, apartamento"}),
            "reference": forms.TextInput(attrs={"placeholder": "Ej.: frente al parque, portón verde"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["province"].choices = [("", "Selecciona una provincia")] + list(self.fields["province"].choices)[1:]
        self.fields["province"].widget.attrs["autocomplete"] = "address-level1"

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 7:
            raise forms.ValidationError("Escribe un teléfono de al menos 7 dígitos, por ejemplo 6123-4567.")
        return phone

    def clean(self):
        data = super().clean()
        if data.get("shipping_method") == ShippingMethod.CIUDAD and data.get("province") not in (None, "", "panama", "panama-oeste"):
            self.add_error(
                "shipping_method",
                "El envío a Ciudad de Panamá solo aplica para Panamá y Panamá Oeste. Elige «Envío al interior» o «Retiro en tienda».",
            )
        if data.get("payment_method") == PaymentMethod.CONTRA_ENTREGA and data.get("shipping_method") != ShippingMethod.CIUDAD:
            self.add_error(
                "payment_method",
                "El pago contra entrega solo está disponible con envío en Ciudad de Panamá. Elige otro método de pago.",
            )
        return data


class OrderStatusForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status", "notes"]
        labels = {"status": "Estado del pedido", "notes": "Notas internas"}
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
