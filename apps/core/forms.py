from django import forms

from .models import ContactMessage


class StyledFormMixin:
    """Asigna las clases del sistema visual a cada widget y enlaza errores con aria."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput,)):
                css = "checkbox"
            elif isinstance(widget, (forms.RadioSelect, forms.CheckboxSelectMultiple)):
                css = ""
            elif isinstance(widget, forms.Select):
                css = "select"
            elif isinstance(widget, forms.Textarea):
                css = "input min-h-32"
                widget.attrs.setdefault("rows", 5)
            elif isinstance(widget, forms.ClearableFileInput):
                css = "file-input"
            else:
                css = "input"
            if css:
                widget.attrs["class"] = f"{css} {widget.attrs.get('class', '')}".strip()
            if field.help_text:
                widget.attrs["aria-describedby"] = f"{self[name].auto_id}_help"

    def full_clean(self):
        # Marca los errores tras validar; hacerlo en __init__ validaba antes de que las subclases configuraran sus campos.
        super().full_clean()
        for name in self.errors:
            if name in self.fields:
                attrs = self.fields[name].widget.attrs
                attrs["aria-invalid"] = "true"
                attrs["aria-describedby"] = f"{attrs.get('aria-describedby', '')} {self[name].auto_id}_error".strip()


class ContactForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "topic", "message"]
        labels = {"name": "Nombre", "email": "Correo", "topic": "¿Sobre qué nos escribes?", "message": "Mensaje"}
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
        }
