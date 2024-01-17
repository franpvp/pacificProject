from django.db import models

# Create your models here.

# Lista de opciones para variable "tipo_usuario"
class TipoUsuario(models.Model):
    id_tipo_usuario = models.IntegerField(primary_key=True, unique=True)
    nombre_tipo_usuario = models.CharField(max_length=20, verbose_name="Nombre tipo usuario")

    def __str__(self):
        return self.nombre_tipo_usuario

class RegistroUsuario(models.Model):
    id_user = models.AutoField(primary_key=True, unique=True,verbose_name="Id usuario")
    nombres = models.CharField(max_length=50, verbose_name="Nombres del usuario")
    apellidos = models.CharField(max_length=50, verbose_name="Apellidos del usuario")
    correo = models.EmailField(max_length=50, verbose_name="Correo de usuario")
    nombre_usuario = models.CharField(max_length=25, verbose_name="Nombre de usuario")
    direccion = models.CharField(max_length=60, verbose_name="Dirección de usuario")

    def __str__(self):
        return self.nombres

class ReporteReserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, unique=True, verbose_name="Id reserva")
    dia_ingreso = models.DateField(auto_now_add=True)
    hora_ingreso = models.TimeField(auto_now=True)
    dia_salida = models.DateField()
    hora_salida = models.TimeField()

    def __str__(self):
        return f"{self.dia_ingreso} - {self.hora_ingreso}"



