from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from apps.core.forms import StyledFormMixin

from .models import Profile

User = get_user_model()


class LoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "autofocus": True}),
    )
    password = forms.CharField(
        label="Contraseña", strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_login": "El correo o la contraseña no coinciden. Revisa ambos e inténtalo de nuevo.",
        "inactive": "Esta cuenta está desactivada.",
    }


class RegisterForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=60, widget=forms.TextInput(attrs={"autocomplete": "given-name"}))
    last_name = forms.CharField(label="Apellido", max_length=60, widget=forms.TextInput(attrs={"autocomplete": "family-name"}))
    email = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={"autocomplete": "email"}))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Contraseña"
        self.fields["password1"].help_text = "Mínimo 8 caracteres; evita contraseñas comunes o solo números."
        self.fields["password2"].label = "Repite la contraseña"
        self.fields["password2"].help_text = ""
        for name in ("password1", "password2"):
            self.fields[name].widget.attrs["autocomplete"] = "new-password"
        # password2 ya no tiene ayuda: deja solo la referencia al error, si la hay
        attrs = self.fields["password2"].widget.attrs
        refs = [r for r in attrs.get("aria-describedby", "").split() if not r.endswith("_help")]
        if refs:
            attrs["aria-describedby"] = " ".join(refs)
        else:
            attrs.pop("aria-describedby", None)
        if "aria-describedby" not in self.fields["password1"].widget.attrs:
            self.fields["password1"].widget.attrs["aria-describedby"] = f"{self['password1'].auto_id}_help"

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo. ¿Quieres iniciar sesión?")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class UserInfoForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Nombre", "last_name": "Apellido", "email": "Correo electrónico"}

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(username__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ese correo ya pertenece a otra cuenta.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email
        if commit:
            user.save()
        return user


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "province", "district", "address", "reference"]
        labels = {
            "phone": "Teléfono celular",
            "province": "Provincia",
            "district": "Distrito o corregimiento",
            "address": "Dirección",
            "reference": "Punto de referencia",
        }
        widgets = {"phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["province"].choices = [("", "Selecciona una provincia")] + list(self.fields["province"].choices)[1:]
