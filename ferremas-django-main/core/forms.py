from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Mecanico, Trabajo


class RegisterClienteForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name',"email", 'password1', 'password2']


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", 'password1', 'password2']
class MecanicoForm(forms.ModelForm):
    class Meta:
        model = Mecanico
        fields = [
            "rut",
            "nombre",
            "telefono",
            "fecha_nacimiento",
            "direccion",
            "especialidad"
        ]

class TrabajoForm(forms.ModelForm):
    class Meta:
        model = Trabajo
        fields = [
            "foto_principal",
            "titulo",
            "fecha_trabajo",
            "auto",
            "diagnostico",
            "descripcion",
        ]

class RevisionForm(forms.ModelForm):
    ESTADO_REVISION = (
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado")
    )
    revision = forms.ChoiceField(choices=ESTADO_REVISION)

    class Meta:
        model = Trabajo
        fields = [
            "observaciones",
        ]

