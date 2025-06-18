from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Producto, Trabajador, AdministradorFerreteria

# FORMULARIO DE REGISTRO PARA USUARIOS
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# FORMULARIO USUARIO PERSONALIZADO (si lo usás aparte)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# FORMULARIO CLIENTE
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'telefono', 'email']
        widgets = {
            'rut': forms.TextInput(attrs={'placeholder': 'Ingrese RUT'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej: +56912345678'}),
        }

# FORMULARIO ADMINISTRADOR FERRETERÍA
class AdministradorFerreteriaForm(forms.ModelForm):
    class Meta:
        model = AdministradorFerreteria
        fields = ['rut', 'nombre', 'telefono', 'email']

# FORMULARIO TRABAJADOR
class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'telefono', 'fecha_nacimiento', 'direccion', 'area']

# FORMULARIO PRODUCTO
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['trabajador', 'foto', 'nombre', 'fecha_ingreso', 'marca', 'descripcion', 'precio', 'stock', 'estado', 'observaciones']
