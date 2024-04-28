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
    rol = models.CharField(max_length=20, verbose_name="Rol del usuario", blank=True, null=True, default='Cliente')

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
    order_id = models.CharField(max_length=100, verbose_name="Id Orden PayPal", null=True, blank=True)
    fecha_llegada = models.DateField(null=False, verbose_name="Fecha Llegada")
    fecha_salida = models.DateField(null=False, verbose_name="Fecha Salida")
    cant_adultos = models.IntegerField(verbose_name="Cantidad Adultos", null=False)
    cant_ninos = models.IntegerField(verbose_name="Cantidad Niños", null=True)
    habitacion = models.CharField(max_length=50, verbose_name="Habitacion")
    tipo_metodo_pago = models.CharField(max_length=20, verbose_name="Metodo Pago cliente")
    total = models.IntegerField(verbose_name="Total Reserva")
    pago_inicial = models.IntegerField(verbose_name="Pago Inicial Reserva")
    pago_pendiente = models.IntegerField(verbose_name="Pago Pendiente")
    estado_pago = models.CharField(max_length=20, verbose_name="Estado Pago", default="Pendiente")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.id_user

# Tabla Reporte Reserva
class ReporteReserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, unique=True, verbose_name="Id reserva")
    dia_ingreso = models.DateField(null=False, verbose_name="Dia Ingreso")
    hora_ingreso = models.TimeField(null=True, blank=True)
    dia_salida = models.DateField(null=False, verbose_name="Dia Salida")
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.dia_ingreso} - {self.hora_ingreso}"

    def hacer_checkin(self, hora_checkin):
        self.hora_checkin = hora_checkin
        self.save()

    def hacer_checkout(self, hora_checkout):
        self.hora_checkout = hora_checkout
        self.save()

# Tipo Habitacion (Suite, Premium, Twin)
class TipoHabitacion(models.Model):
    id_tipo_hab = models.AutoField(primary_key=True, unique=True, verbose_name="ID tipo habitación")
    tipo_hab = models.CharField(max_length=25, verbose_name="Tipo habitación")

    def __str__(self):
        return self.tipo_hab

# Tabla Habitaciones
class Habitacion(models.Model):
    id_hab = models.AutoField(primary_key=True, unique=True, verbose_name="Id habitación")
    id_tipo_hab = models.IntegerField(verbose_name="ID tipo habitación")
    titulo_hab = models.CharField(max_length=50, verbose_name="Titulo habitación")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    titulo_en = models.CharField(max_length=50, verbose_name="Titulo habitación en inglés")
    descripcion_en = models.CharField(max_length=200, verbose_name="Descripción en inglés")
    capacidad_max = models.IntegerField(verbose_name="Capacidad Máxima habitación")
    precio = models.CharField(max_length=50, verbose_name="Precio")
    estado = models.CharField(max_length=50, verbose_name="Estado", default='Disponible')
    imagen = models.TextField(null=True, blank=True, verbose_name='Datos de la imagen en base64')

    def __str__(self):
        return self.titulo


class DatosBancarios(models.Model):
    id_banco = models.AutoField(primary_key=True, unique=True, verbose_name="Id Banco")
    beneficiario = models.CharField(max_length=50, verbose_name="Beneficiario")
    cuenta = models.CharField(max_length=50, verbose_name="Cuenta")
    nro_cuenta = models.CharField(max_length=50, verbose_name="Número cuenta bancaria")
    correo_banco = models.CharField(max_length=50, verbose_name="Correo Banco")

    def __str__(self):
        return self.beneficiario


# Tabla Creación Reserva (Con datos cliente)
class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True, unique=True, verbose_name="Id reserva")
    id_user = models.CharField(max_length=20, verbose_name="Id Usuario")
    order_id = models.CharField(max_length=100, verbose_name="Id Orden PayPal", default='')
    fecha_llegada = models.DateField(null=False, verbose_name="Fecha Llegada")
    fecha_salida = models.DateField(null=False, verbose_name="Fecha Salida")
    cant_adultos = models.IntegerField(verbose_name="Cantidad Adultos", null=False)
    cant_ninos = models.IntegerField(verbose_name="Cantidad Niños", null=True)
    tipo_hab = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, verbose_name="Tipo Habitación")
    tipo_metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, verbose_name="Método de Pago cliente")
    total = models.IntegerField(verbose_name="Total Reserva")
    pago_inicial = models.IntegerField(verbose_name="Pago Inicial Reserva")
    pago_pendiente = models.IntegerField(verbose_name="Pago Pendiente")
    estado_pago = models.CharField(max_length=20, verbose_name="Estado Pago", default="Pendiente")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.id_user
    

# Tabla Reporte Reserva
class ReporteReserva(models.Model):
    id_reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, verbose_name="Reserva")
    dia_ingreso = models.DateField(null=False, verbose_name="Dia Ingreso")
    hora_ingreso = models.TimeField(null=True, blank=True)
    dia_salida = models.DateField(null=False, verbose_name="Dia Salida")
    hora_salida = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.dia_ingreso} - {self.hora_ingreso}"

    def hacer_checkin(self, hora_checkin):
        self.hora_checkin = hora_checkin
        self.save()

    def hacer_checkout(self, hora_checkout):
        self.hora_checkout = hora_checkout
        self.save()
