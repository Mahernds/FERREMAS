from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Producto, Trabajador, AdministradorFerreteria

# FORMULARIO DE REGISTRO PARA USUARIOS
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Will be used as your username.")
    user_type = forms.ChoiceField(choices=[('Cliente', 'Cliente'), ('Trabajador', 'Trabajador')], required=True)
    rut = forms.CharField(max_length=10, required=True)
    nombre = forms.CharField(max_length=100, required=True)
    telefono = forms.CharField(max_length=15, required=True)

    # Trabajador specific fields (optional)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    direccion = forms.CharField(max_length=255, required=False)
    area = forms.CharField(max_length=100, required=False, help_text="Applicable if registering as Trabajador.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',
                  'user_type', 'rut', 'nombre', 'telefono',
                  'fecha_nacimiento', 'direccion', 'area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].required = False
            self.fields['username'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        # Ensure username is populated even if it was initially missing (e.g. due to being hidden)
        # UserCreationForm's validation might still require a username value.
        if email and not cleaned_data.get('username'):
            cleaned_data['username'] = email

        # Check for username uniqueness based on email
        if email:
            if User.objects.filter(username=email).exists():
                self.add_error('email', "A user with this email (username) already exists.")
        return cleaned_data

    # UserCreationForm's save() method will now use the username (populated from email)
    # from cleaned_data. No need to override save() for this specific purpose.

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
