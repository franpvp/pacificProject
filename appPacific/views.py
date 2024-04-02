from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import RegistroUsuario, TipoUsuario, ReporteReserva, Habitacion, TipoHabitacion
from django.http import HttpResponse
from .forms import RegistroUsuarioAdminForm
import binascii
import requests
import base64

# Create your views here.

# Vista Index
def index(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellido')
        rut = request.POST.get('rut')
        correo = request.POST.get('correo')
        celular = request.POST.get('celular')
        contrasena = request.POST.get('password')
        conf_contrasena = request.POST.get('password2')
        
    return render(request, 'app/index.html')

# Vista Home
def home(request):
    return render(request,'app/home.html')

# Vista Login
def login(request):
    return render(request, 'app/login.html')

# Vista Registro
def registro(request):
    return render(request, 'registration/registro.html')

# Vista Contacto
def contacto(request):
    return render(request, 'app/contacto.html')


# Vista Habitaciones
def habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'app/habitaciones.html', {'habitaciones': habitaciones})

# Vista Método Pago
def metodo_pago(request):
    return render(request, 'app/metodo_pago.html')

# Vista Reserva Realizada
def reserva_realizada(request):
    return render(request, 'app/reserva_realizada.html')

# Vista Nosotros
def nosotros(request):
    return render(request, 'app/nosotros.html')

# Vista Administrador Home
def administrador_home(request):
    return render(request, 'administrador/administrador_home.html')

# Vista Administrador Gestion Habitaciones
def gestion_habitaciones(request):
    return render(request, 'administrador/gestion_habitaciones.html')

# Vista Administrador Gestion Habitaciones -crear
def crear_habitacion(request):
    if request.method == 'POST':
        id_tipo_hab = request.POST.get('id_tipo_hab')
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        imagen_bytes = request.FILES.get('cargarImagen').read()

        # Codificar los bytes de la imagen en base64
        imagen_base64 = base64.b64encode(imagen_bytes)
        imagen_base64_str = imagen_base64.decode('utf-8')

        # Buscar el objeto TipoHabitacion con el ID proporcionado (Esto trae Suite, Premium o Twin)
        # tipo_habitacion = TipoHabitacion.objects.get(id_tipo_hab=id_tipo_hab) 

        # Crear la instancia de Habitacion con la imagen codificada en base64
        habitacion = Habitacion(
            id_tipo_hab=id_tipo_hab,
            titulo=titulo,
            descripcion=descripcion,
            cantidad=cantidad,
            precio=precio,
            imagen=imagen_base64_str  # Almacenar la imagen codificada en base64
        )

        # Guardar la instancia en la base de datos
        habitacion.save()

        # Mostrar un mensaje de éxito
        messages.success(request, '¡La habitación se creó exitosamente!')
    return render(request, 'administrador/gestion_habitaciones/crear_habitacion.html')


# Vista Administrador Gestion Habitaciones-eliminar
def eliminar_habitacion(request):
    if request.method == 'POST':
        id_hab = request.POST.get('id_hab')
        habitacion = Habitacion.objects.get(id_hab=id_hab)
        habitacion.delete()
    # Se obtienen todos los registros de habitaciones
    habitaciones = Habitacion.objects.all()

    return render(request, 'administrador/gestion_habitaciones/eliminar_habitacion.html', {'habitaciones': habitaciones})

# Vista Administrador Gestion Habitaciones-modificar
def modificar_habitacion(request):
    if request.method == 'POST':
        id_hab = request.POST.get('id_hab')
        id_tipo_hab = request.POST.get('id_tipo_hab')
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')

        habitacion = Habitacion.objects.get(id_hab=id_hab)

        # Actualizar los campos de la habitación
        habitacion.id_tipo_hab = id_tipo_hab
        habitacion.titulo = titulo
        habitacion.descripcion = descripcion
        habitacion.cantidad = cantidad
        habitacion.precio = precio

        habitacion.save()
    habitaciones = Habitacion.objects.all();
    return render(request, 'administrador/gestion_habitaciones/modificar_habitacion.html', {'habitaciones': habitaciones})

# Vista Administrador Gestion Habitaciones-ver
def ver_habitacion(request):
    habitaciones = Habitacion.objects.all()

    return render(request, 'administrador/gestion_habitaciones/ver_habitacion.html',{'habitaciones':habitaciones})

# Vista Administrador Gestion Reservas
def gestion_reservas(request):
    return render(request, 'administrador/gestion_reservas.html')

# Vista Administrador Gestion Reservas -crear
def crear_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/crear_reserva_pacific.html')

# Vista Administrador Gestion Reservas -eliminar
def eliminar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/eliminar_reserva_pacific.html')

# Vista Administrador Gestion Reservas -modificar
def modificar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/modificar_reserva_pacific.html')

# Vista Administrador Gestion Reservas -ver calendario
def ver_calendario_pacific(request):
    return render(request, 'administrador/gestion_reservas/ver_calendario_pacific.html')

# Vista Administrador Gestion Reservas -ver reserva
def ver_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/ver_reserva_pacific.html')

# Vista Administrador Gestion Usuarios
def gestion_usuarios(request):
    return render(request, 'administrador/gestion_usuarios.html')

# Vista Administrador Gestion Usuarios -crear usuario
def crear_usuario(request):
    return render(request, 'administrador/gestion_usuarios/crear_usuario.html')

# Vista Administrador Gestion Usuarios -eliminar usuario
def eliminar_usuario(request):
    return render(request, 'administrador/gestion_usuarios/eliminar_usuario.html')

# Vista Administrador Gestion Usuarios modificar usuario
def modificar_usuario(request):
    return render(request, 'administrador/gestion_usuarios/modificar_usuario.html')
    
# Vista Administrador Gestion Usuarios -ver usuario
def ver_usuario(request):
    return render(request, 'administrador/gestion_usuarios/ver_usuario.html')

def crear_usuario_admin(request):
    if request.method == 'POST':
        form = RegistroUsuarioAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios_admin')
    else:
        form = RegistroUsuarioAdminForm()

    return render(request, 'administrador/gestion_usuarios/crear_usuario.html', {'form': form})

def ver_usuarios_admin(request):
    usuarios = RegistroUsuario.objects.all()
    return render(request, 'administrador/gestion_usuarios/ver_usuario.html', {'usuarios': usuarios})

def modificar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario) 
    if request.method == 'POST':
        form = RegistroUsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios_admin')
    else:
        form = RegistroUsuarioAdminForm(instance=usuario)
    return render(request, 'administrador/gestion_usuarios/modificar_usuario.html', {'form': form})

def eliminar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuarios_admin')
    return render(request, 'administrador/gestion_usuarios/eliminar_usuario.html', {'usuario': usuario})

