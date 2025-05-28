from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Trabajador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=100, primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100)
    area = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.nombre}, área: {self.area}"


class Producto(models.Model):
    ESTADO = (
        ("Disponible", "Disponible"),
        ("Sin stock", "Sin stock"),
        ("Descontinuado", "Descontinuado"),
    )

    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='productos/', null=True)
    nombre = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    fecha_actualizacion = models.DateField(auto_now=True)
    marca = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    estado = models.CharField(max_length=100, choices=ESTADO)
    observaciones = models.TextField(null=True, blank=True)


class AdministradorFerreteria(models.Model):
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






