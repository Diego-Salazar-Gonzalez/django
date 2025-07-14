# catalogo/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente
from django.contrib.auth import authenticate


class RegistroClienteForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Correo o contraseña incorrectos")
            if not user.is_active:
                raise forms.ValidationError("Cuenta inactiva")
            cleaned_data['user'] = user
        return cleaned_data