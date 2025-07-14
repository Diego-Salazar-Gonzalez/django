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
    email = forms.EmailField(label='Correo', widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-cyan-200 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-400 text-black',
        'placeholder': 'ejemplo@correo.com'
    }))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-cyan-200 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-400 text-black',
        'placeholder': '********'
    }))