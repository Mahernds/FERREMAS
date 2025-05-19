from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Especialidad(models.Model):
    nombre_especialidad = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre_especialidad



class Mecanico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)

    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nombre + ", especialidad: " + self.especialidad.__str__()

class Trabajo(models.Model):
    ESTADO_REVISION = (
        ("Por revisar", "Por revisar"),
        ("Aprobado", "Aprobado"),
        ("Rechazado", "Rechazado"),
        ("Inactivo", "Inactivo"),
    )

    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)
    foto_principal = models.ImageField(upload_to='fotos/', null=True)
    #fotos_secundarias
    titulo = models.CharField(max_length=100, null=True)
    fecha_trabajo = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateField(auto_now=True, null=True)
    auto = models.CharField(max_length=100)
    diagnostico = models.CharField(max_length=150)
    descripcion = models.TextField()

    revision = models.CharField(max_length=100, choices=ESTADO_REVISION)
    observaciones = models.TextField(null=True, blank=True)

class AdministradorTaller(models.Model):
    rut = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Cliente(models.Model):
    rut = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)







