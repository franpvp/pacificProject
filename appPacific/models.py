from django.db import models

# Create your models here.

# Lista de opciones para variable "tipo_usuario"
class TipoUsuario(models.Model):
    id_tipo_usuario = models.IntegerField(primary_key=True, unique=True)
    nombre_tipo_usuario = models.CharField(max_length=20, verbose_name="Nombre tipo usuario")

    def __str__(self):
        return self.nombre_tipo_usuario

class RegistroUsuario(models.Model):
    id_user = models.AutoField(primary_key=True, unique=True, verbose_name="Id usuario")
    nombres = models.CharField(max_length=50, verbose_name="Nombres del usuario")
    apellidos = models.CharField(max_length=50, verbose_name="Apellidos del usuario")
    correo = models.EmailField(max_length=50, verbose_name="Correo del usuario")
    telefono = models.CharField(max_length=25, verbose_name="Teléfono del usuario", default='')
    contrasena = models.CharField(max_length=25, verbose_name="Contraseña del usuario", default='')
    rol = models.CharField(max_length=20, verbose_name="Rol del usuario", default='Cliente')

    def __str__(self):
        return self.nombres

class MetodoPago(models.Model):
    id_metodo_pago = models.AutoField(primary_key=True, unique=True, verbose_name="Id Metodo Pago")
    tipo_metodo_pago = models.CharField(max_length=20, verbose_name="Metodo Pago")

    def __str__(self):
        return self.tipo_metodo_pago

# Tabla Creación Reserva (Con datos cliente)
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, unique=True, verbose_name="Id reserva")
    id_user = models.CharField(max_length=20, verbose_name="Id Usuario")
    fecha_llegada = models.DateField(null=False, verbose_name="Fecha Llegada")
    fecha_salida = models.DateField(null=False, verbose_name="Fecha Salida")
    cant_adultos = models.IntegerField(verbose_name="Cantidad Adultos", null=False)
    cant_ninos = models.IntegerField(verbose_name="Cantidad Niños", null=True)
    
    tipo_metodo_pago = models.CharField(max_length=20, verbose_name="Metodo Pago cliente")
    pago_reserva = models.IntegerField(verbose_name="Pago Reserva")
    total_restante = models.IntegerField(verbose_name="Total Restante")
    estado_pago = models.CharField(max_length=20, verbose_name="Estado Pago", default="Pendiente")

    def __str__(self):
            return self.id_user

# Tabla Reporte Reserva
class ReporteReserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, unique=True, verbose_name="Id reserva")
    dia_ingreso = models.DateField(auto_now_add=True)
    hora_ingreso = models.TimeField(auto_now=True)
    dia_salida = models.DateField()
    hora_salida = models.TimeField()

    def __str__(self):
        return f"{self.dia_ingreso} - {self.hora_ingreso}"

# Tipo Habitacion (Suite, Premium, Twin)
class TipoHabitacion(models.Model):
    id_tipo_hab = models.IntegerField(primary_key=True, unique=True, verbose_name="ID tipo habitación")
    tipo_hab = models.CharField(max_length=25, verbose_name="Tipo habitación")

    def __str__(self):
        return self.tipo_hab

# Tabla Habitaciones
class Habitacion(models.Model):
    id_hab = models.AutoField(primary_key=True, unique=True, verbose_name="Id habitación")
    id_tipo_hab = models.IntegerField(verbose_name="ID tipo habitación")
    titulo = models.CharField(max_length=50, verbose_name="Titulo habitación")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    cantidad = models.CharField(max_length=50, verbose_name="Cantidad Habitaciones")
    precio = models.CharField(max_length=50, verbose_name="Precio")
    imagen = models.TextField(null=True, blank=True, verbose_name='Datos de la imagen en base64')

    def __str__(self):
        return self.titulo



