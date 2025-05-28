from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import Group, User

from . import models
from .forms import ClienteForm, TrabajadorForm, UserForm, ProductoForm
from .decorators import unauthenticated_user, allowed_users
from .models import Trabajador, Producto

def index(request):
    productos_destacados = Producto.objects.filter(estado="Disponible").order_by('-fecha_ingreso')[:3]
    producto_destacado = productos_destacados[0] if productos_destacados else None
    otros_productos = productos_destacados[1:] if productos_destacados.count() > 1 else []

    context = {
        "producto_destacado": producto_destacado,
        "otros_productos": otros_productos
    }
    return render(request, 'landing.html', context)

def nosotros(request):
    return render(request, 'nosotros.html')

@unauthenticated_user
def login(request):
    cliente_form = ClienteForm()
    context = {'cliente_form': cliente_form}

    if request.method == 'POST':
        if "register" in request.POST:
            cliente_form = ClienteForm(request.POST)
            if cliente_form.is_valid():
                user = User.objects.create_user(
                    username=cliente_form.cleaned_data['email'],
                    email=cliente_form.cleaned_data['email'],
                    password='default1234',
                    first_name=cliente_form.cleaned_data['nombre'],
                )
                group = Group.objects.get(name='cliente')
                user.groups.add(group)
                user.save()

                cliente = cliente_form.save(commit=False)
                cliente.user = user
                cliente.save()

                messages.success(request, 'Cliente registrado con éxito.')
                return redirect("/login")

        if "login" in request.POST:
            username = request.POST['login_email']
            password = request.POST['login_password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect("/auth_error")
            else:
                messages.error(request, "Correo o contraseña incorrectos.")

    return render(request, 'session.html', context)

def user_logout(request):
    logout(request)
    return redirect('/')

def auth_error(request):
    if not request.user.groups.exists():
        return redirect("/")

    group = request.user.groups.all()[0].name

    if group == "administrador_ferreteria":
        return redirect("/admin_ferreteria")
    if group == "cliente":
        return redirect("/")
    if group == "trabajador":
        return redirect("/admin_trabajador")

    return redirect("/")

def productos(request):
    productos_disponibles = Producto.objects.filter(estado="Disponible")

    if "trabajador" in request.GET:
        trabajador = Trabajador.objects.filter(nombre=request.GET['trabajador']).first()
        if trabajador:
            productos_disponibles = productos_disponibles.filter(trabajador=trabajador)
        else:
            productos_disponibles = Producto.objects.none()

    return render(request, 'productos.html', {"productos": productos_disponibles})

def ver_producto(request, pk):
    producto = Producto.objects.get(id=pk)
    return render(request, "trabajos/trabajo-{}.html".format(pk), {"producto": producto})

def trabajos(request):
    return render(request, "trabajos.html")

@allowed_users(allowed_roles=['administrador_ferreteria'])
def admin_ferreteria(request):
    context = {
        "trabajadores": Trabajador.objects.all(),
        "productos": Producto.objects.all(),
    }
    return render(request, "admin-ferreteria.html", context)

@allowed_users(allowed_roles=['administrador_ferreteria'])
def admin_ferreteria_crear_trabajador(request):
    trabajador_form = TrabajadorForm()
    user_form = UserForm()

    if request.method == "POST":
        trabajador_form = TrabajadorForm(request.POST, prefix='trabajador_form')
        user_form = UserForm(request.POST, prefix='user_form')

        if trabajador_form.is_valid() and user_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['email'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password'],
                first_name=trabajador_form.cleaned_data['nombre'],
            )

            group = Group.objects.get(name='trabajador')
            user.groups.add(group)
            user.save()

            trabajador = trabajador_form.save(commit=False)
            trabajador.user = user
            trabajador.save()

            return redirect("/admin_ferreteria")

    context = {"user_form": user_form, 'trabajador_form': trabajador_form}
    return render(request, "admin-ferreteria-crear-trabajador.html", context)

@allowed_users(allowed_roles=['administrador_ferreteria'])
def admin_ferreteria_eliminar_trabajador(request, pk):
    trabajador = Trabajador.objects.get(rut=pk)
    user = trabajador.user

    if request.method == "POST":
        user.delete()
        trabajador.delete()
        return redirect("/admin_ferreteria")

    return render(request, "admin-ferreteria-eliminar-trabajador.html", {"trabajador": trabajador})

@allowed_users(allowed_roles=['trabajador'])
def admin_trabajador(request):
    trabajador = Trabajador.objects.get(user=request.user)
    productos = Producto.objects.filter(trabajador=trabajador)
    return render(request, "admin-trabajador.html", {"productos": productos})

@allowed_users(allowed_roles=['trabajador'])
def admin_trabajador_nuevo_producto(request):
    form = ProductoForm()

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.trabajador = Trabajador.objects.get(user=request.user)
            producto.estado = "Disponible"
            producto.save()
            return redirect("/admin_trabajador")

    return render(request, "admin-trabajador-nuevo-producto.html", {"form": form})

@allowed_users(allowed_roles=['trabajador'])
def admin_trabajador_modificar_producto(request, pk):
    producto = Producto.objects.get(id=pk)
    form = ProductoForm(instance=producto)

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect("/admin_trabajador")

    return render(request, "admin-trabajador-nuevo-producto.html", {"form": form})

@allowed_users(allowed_roles=['trabajador'])
def admin_trabajador_eliminar_producto(request, pk):
    producto = Producto.objects.get(id=pk)

    if request.method == "POST":
        producto.delete()
        return redirect("/admin_trabajador")

    return render(request, "admin-trabajador-eliminar-producto.html", {"producto": producto})
