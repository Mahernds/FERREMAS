from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.template import loader
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm
from django.urls import reverse # Ensure reverse is imported

from django.contrib.auth import authenticate, login as auth_login, logout # auth_login is already here
from django.contrib.auth.models import Group, User

from . import models
from .models import Cliente, Trabajador, Categoria, Producto # Ensure Cliente, Categoria are imported
from .forms import ClienteForm, TrabajadorForm, UserForm, ProductoForm
from .decorators import unauthenticated_user, allowed_users


def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # The form's save method now handles setting username from email.
            user = form.save()

            user_type = form.cleaned_data.get('user_type')
            rut = form.cleaned_data.get('rut')
            nombre = form.cleaned_data.get('nombre')
            telefono = form.cleaned_data.get('telefono')
            # email = form.cleaned_data.get('email') # email is already part of user object

            try:
                if user_type == 'Cliente':
                    Cliente.objects.create(
                        user=user,
                        rut=rut,
                        nombre=nombre,
                        telefono=telefono,
                        email=user.email # Use user.email as it's saved by form.save()
                    )
                    group, _ = Group.objects.get_or_create(name='cliente')
                    user.groups.add(group)
                    messages.success(request, 'Cliente registrado con éxito.')

                elif user_type == 'Trabajador':
                    area_nombre = form.cleaned_data.get('area')
                    area_obj = None
                    if area_nombre: # Only try to get/create if area_nombre is provided
                        area_obj, _ = Categoria.objects.get_or_create(nombre=area_nombre)

                    Trabajador.objects.create(
                        user=user,
                        rut=rut,
                        nombre=nombre,
                        telefono=telefono,
                        # email field is not in Trabajador model
                        fecha_nacimiento=form.cleaned_data.get('fecha_nacimiento'),
                        direccion=form.cleaned_data.get('direccion'),
                        area=area_obj
                    )
                    group, _ = Group.objects.get_or_create(name='trabajador')
                    user.groups.add(group)
                    messages.success(request, 'Trabajador registrado con éxito.')

                auth_login(request, user) # Log in the user
                return redirect('inicio')
            except Exception as e:
                # If profile creation or group assignment fails, it's good to delete the user
                # to allow them to try registering again.
                user.delete()
                messages.error(request, f'Error al crear el perfil de usuario: {e}')
                # Fall through to re-render the form with an error
        # If form is not valid, it will fall through to re-render the form with errors
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

# This is a standard login view, perhaps used by admin or other parts.
# The subtask is to refactor login_custom.
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # login(request, user) was here, but auth_login is the standard alias
            auth_login(request, user)
            return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request): # This is the one to keep
    logout(request)
    return redirect('login')

def inicio(request):
    productos_disponibles = Producto.objects.filter(estado="Disponible").order_by('-fecha_ingreso')
    
    ultimo_trabajo = productos_disponibles.first()
    sig_trabajos = productos_disponibles[1:3] if productos_disponibles.count() > 1 else []

    context = {
        'ultimo_trabajo': ultimo_trabajo,
        'sig_trabajos': sig_trabajos
    }
    return render(request, 'landing.html', context)


def nosotros(request):
    return render(request, 'nosotros.html')

from django.views.decorators.http import require_POST # This import is fine here

@require_POST
def agregar_al_carrito(request, producto_id):
    # This JsonResponse is not defined here. It should be: from django.http import JsonResponse
    # However, this part of the code is not being touched by the current subtask.
    # For now, I will assume JsonResponse is imported at the top, as per previous file states.
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)

    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1
    request.session['carrito'] = carrito
    return JsonResponse({'contador': sum(carrito.values())})

def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        productos.append({'producto': producto, 'cantidad': cantidad})
        total += producto.precio * cantidad

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total,
        'contador_carrito': sum(carrito.values())
    })

def session(request):
    return render(request, 'session.html')


@unauthenticated_user
def login_custom(request): # Refactored login_custom
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(reverse('auth_error'))
        # If form is not valid, it will fall through to render with the form containing errors.
    else:
        form = AuthenticationForm()
    # For GET request or if POST form is invalid, pass the form to the template.
    return render(request, 'login.html', {'form': form})

# user_logout view is removed. logout_usuario is the standard.

def auth_error(request):
    # Added is_authenticated check for robustness from previous branch work
    if not request.user.is_authenticated:
        return redirect('login')

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
    productos = Producto.objects.all()
    carrito = request.session.get('carrito', {})
    return render(request, 'productos.html', {
        'productos': productos,
        'contador_carrito': sum(carrito.values())
    })

def ver_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "ver-producto.html", {"producto": producto})

def trabajos(request):
    return render(request, "trabajos.html")

# Admin Ferretería views remain unchanged for this subtask
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


# Admin Trabajador views remain unchanged for this subtask
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
