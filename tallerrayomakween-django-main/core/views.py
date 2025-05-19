from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import loader

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import Group, User

from . import models
from .forms import RegisterClienteForm, MecanicoForm, UserForm, TrabajoForm, RevisionForm
from .decorators import unauthenticated_user, allowed_users
from .models import Mecanico, Trabajo

# Create your views here.
def index(request):
    ultimos_trabajos = Trabajo.objects.filter(revision="Aprobado").order_by('fecha_creacion')[:3]
    ultimo_trabajo = ultimos_trabajos[0]
    sig_trabajos = ultimos_trabajos[1:]
    context = {"ultimo_trabajo": ultimo_trabajo,
               "sig_trabajos": sig_trabajos
               }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

def nosotros(request):
    template = loader.get_template('nosotros.html')
    return HttpResponse(template.render({}, request))


@unauthenticated_user
def login(request):
    register_form = RegisterClienteForm()
    context = {'register_form': register_form}
    template = loader.get_template('login.html')

    if request.method == 'POST':
        if "register" in request.POST:
            user_creation_form = RegisterClienteForm(request.POST)
            if user_creation_form.is_valid():
                #creamos el usuario de forma manual
                user = User.objects.create_user(username=user_creation_form.cleaned_data['email'],
                                                email=user_creation_form.cleaned_data['email'],
                                                password=user_creation_form.cleaned_data['password1'],
                                                first_name=user_creation_form.cleaned_data['first_name'],)

                # asignamos el grupo "cliente"
                group_cliente = Group.objects.get(name='cliente')
                user.groups.add(group_cliente)

                user.save()
                messages.success(request, 'Registrado con exito!')
                return redirect("/login")

        if "login" in request.POST:
            username = request.POST['login_email']
            password = request.POST['login_password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login exitoso!')
                return redirect("/auth_error")
            else:
                messages.info(request, "Correo o Contraseña incorrectos")

    return HttpResponse(template.render(context, request))

def user_logout(request):
    logout(request)
    return redirect('/')

def auth_error(request):
    if not request.user.groups.exists():
        return redirect("/")

    group = request.user.groups.all()[0].name
    print(group)
    if group == "administrador_taller":
        return redirect("/admin_taller")
    if group == "cliente":
        return redirect("/")
    if group == "mecanico":
        return redirect("/admin_mecanico")

    if group == "superuser":
        return redirect("/admin")

    return redirect("/")

def nuestros_trabajos(request):
    trabajos_validos = Trabajo.objects.filter(revision="Aprobado")
    #procesamos las querys de busqueda

    #busqueda por mecanico
    if "m" in request.GET:
        mecanico = Mecanico.objects.filter(nombre=request.GET['m']).first()

        if mecanico:
            trabajos_validos = trabajos_validos.filter(mecanico = mecanico)
        else:
            trabajos_validos = None

    context = {'trabajos': trabajos_validos}
    template = loader.get_template('trabajos.html')
    return HttpResponse(template.render(context, request))


def ver_trabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    context = {'trabajo': trabajo}
    return render(request,"ver-trabajo.html",context)

def productos(request):
    template = loader.get_template('productos.html')
    return HttpResponse(template.render({}, request))

#####################################################################
# Vistas del Administrador del Taller
#####################################################################
@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller(request):
    context={
        "mecanicos" : Mecanico.objects.all(),
        "trabajos" : Trabajo.objects.all(),
    }
    return render(request,"admin-taller.html",context)

@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller_crearcuenta(request):
    mecanico_form = MecanicoForm()
    user_form = UserForm()
    if request.method == "POST":
        mecanico_form = MecanicoForm(request.POST, prefix='mecanico_form')
        user_form = UserForm(request.POST, prefix='user_form')
        #print(1)
        #print(mecanico_form.is_valid(), user_form.is_valid())
        if mecanico_form.is_valid() and user_form.is_valid():
            #print(2)
            #creamos el nuevo usuario
            user = User.objects.create_user(username=user_form.cleaned_data['email'],
                                            email=user_form.cleaned_data['email'],
                                            password=user_form.cleaned_data['password1'],
                                            first_name=mecanico_form.cleaned_data['nombre'], )
            # asignamos el grupo "cliente"
            group_mecanico = Group.objects.get(name='mecanico')
            user.groups.add(group_mecanico)
            user.save()
            #creamos el mecanico y asignamos su usuario
            mecanico = Mecanico.objects.create(user=user,
                                               rut=mecanico_form.cleaned_data['rut'],
                                               nombre=mecanico_form.cleaned_data['nombre'],
                                               telefono=mecanico_form.cleaned_data['telefono'],
                                               fecha_nacimiento=mecanico_form.cleaned_data['fecha_nacimiento'],
                                               direccion=mecanico_form.cleaned_data['direccion'],
                                               especialidad=mecanico_form.cleaned_data['especialidad']
                                               )
            mecanico.save()
            return redirect("/admin_taller")

    context = {"user_form": user_form,
               'mecanico_form': mecanico_form}
    return render(request, "admin-taller-crearcuenta.html", context)

@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller_actualizarcuenta(request, pk):
    mecanico = Mecanico.objects.get(rut=pk)
    user = mecanico.user

    mecanico_form = MecanicoForm(instance=mecanico)

    if request.method == "POST":
        mecanico_form = MecanicoForm(request.POST, instance=mecanico)
        if mecanico_form.is_valid():
            mecanico_form.save()
            return redirect("/admin_taller")

    context = {'mecanico_form': mecanico_form}
    return render(request, "admin-taller-crearcuenta.html", context)

@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller_borrarcuenta(request, pk):
    mecanico = Mecanico.objects.get(rut=pk)
    user = mecanico.user
    context ={"mecanico" : mecanico,
              "user" : user
              }

    if request.method == "POST":
        print(mecanico)
        user.delete()
        mecanico.delete()
        return redirect("/admin_taller")

    return render(request, "admin-taller-borrarcuenta.html", context)


@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller_revisartrabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    revision_form = RevisionForm(instance=trabajo)
    context = {"trabajo" : trabajo,
               "revision_form": revision_form}

    if request.method == "POST":
        revision_form = RevisionForm(request.POST)
        if revision_form.is_valid():
            trabajo = Trabajo.objects.get(id=pk)
            trabajo.revision = revision_form.cleaned_data['revision']
            trabajo.observaciones = revision_form.cleaned_data['observaciones']
            trabajo.save()
            return redirect("/admin_taller")
    return render(request, "admin-taller-revisartrabajo.html", context)

@allowed_users(allowed_roles=['administrador_taller'])
def admin_taller_trabajos(request):
    context={
        "trabajos" : Trabajo.objects.all(),
    }
    return render(request,"admin-taller-trabajos.html",context)
#####################################################################
# Vistas del Mecanico
#####################################################################
@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico(request):
    mecanico_actual = Mecanico.objects.filter(user=request.user).first()
    trabajos = Trabajo.objects.filter(mecanico = mecanico_actual)
    context = {"trabajos":trabajos}
    return render(request, "admin-mecanico.html", context)


@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_trabajos(request):
    trabajos = Trabajo.objects.all()
    context = {"trabajos":trabajos}
    return render(request, "admin-mecanico-trabajos.html", context)

@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_nuevotrabajo(request):
    trabajo_form = TrabajoForm()
    context = {"trabajo_form": trabajo_form}

    if request.method == "POST":
        trabajo_form = TrabajoForm(request.POST, request.FILES)
        print(1)
        print(trabajo_form.errors.as_data())
        if trabajo_form.is_valid():
            print(2)
            mecanico = Mecanico.objects.get(user=request.user)
            trabajo = Trabajo.objects.create(
                mecanico = mecanico,
                titulo=trabajo_form.cleaned_data['titulo'],
                foto_principal=trabajo_form.cleaned_data['foto_principal'],
                fecha_trabajo=trabajo_form.cleaned_data['fecha_trabajo'],
                auto=trabajo_form.cleaned_data['auto'],
                diagnostico=trabajo_form.cleaned_data['diagnostico'],
                descripcion=trabajo_form.cleaned_data['descripcion'],
                revision="Por revisar",
            )
            trabajo.save()
            print(trabajo)
            return redirect("/admin_mecanico")

    return render(request, "admin-mecanico-nuevotrabajo.html", context)
@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_vertrabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    context = {"trabajo": trabajo}
    return render(request, "admin-mecanico-vertrabajo.html", context)

@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_modtrabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    trabajo_form = TrabajoForm(instance=trabajo)

    if request.method == "POST":
        trabajo_form = TrabajoForm(request.POST, request.FILES, instance=trabajo)
        if trabajo_form.is_valid():
            trabajo_form.save()
            return redirect("/admin_mecanico")

    context = {'trabajo_form': trabajo_form}
    return render(request, "admin-mecanico-nuevotrabajo.html", context)


@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_eliminartrabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    context = {"trabajo": trabajo}

    if request.method == "POST":
        trabajo.delete()
        return redirect("/admin_mecanico")

    return render(request, "admin-mecanico-eliminartrabajo.html", context)
@allowed_users(allowed_roles=['mecanico'])
def admin_mecanico_arreglartrabajo(request, pk):
    trabajo = Trabajo.objects.get(id=pk)
    trabajo_form = TrabajoForm(instance=trabajo)
    context = {"trabajo_form":trabajo_form,
               "trabajo":trabajo}

    if request.method == "POST":
        trabajo_form = TrabajoForm(request.POST, request.FILES, instance=trabajo)
        if trabajo_form.is_valid():
            trabajo_form.save()
            trabajo.revision = "Por revisar"
            trabajo.save()
            return redirect("/admin_mecanico")

    return render(request, "admin-mecanico-arreglartrabajo.html", context)