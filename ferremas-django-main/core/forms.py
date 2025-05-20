from django import forms
from django.contrib.auth.models import User
from .models import Cliente, Producto, Trabajador, AdministradorFerreteria


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['rut', 'nombre', 'telefono', 'email']


class AdministradorFerreteriaForm(forms.ModelForm):
    class Meta:
        model = AdministradorFerreteria
        fields = ['rut', 'nombre', 'telefono', 'email']


class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['rut', 'nombre', 'telefono', 'fecha_nacimiento', 'direccion', 'area']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['trabajador', 'foto', 'nombre', 'fecha_ingreso', 'marca', 'descripcion', 'precio', 'stock', 'estado', 'observaciones']
