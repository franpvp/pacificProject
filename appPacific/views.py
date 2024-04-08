from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import RegistroUsuario, TipoUsuario, ReporteReserva, Habitacion, TipoHabitacion
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistroUsuarioAdminForm
import binascii
import requests
import base64
import re
from django.utils.translation import gettext as _
from .decorators import admin_required
from urllib.parse import urlencode
from django.db import connection

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
        
    habitaciones = Habitacion.objects.all()
    return render(request, 'app/index.html', {'habitaciones': habitaciones})

def registro(request):

    if request.method == 'POST':
        try:
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            correo = request.POST['correo']
            usuario = request.POST['username']
            celular = request.POST['celular']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if not (nombre and apellidos and correo and celular and password1 and password2):
                messages.error(request, _("Por favor, complete todos los campos."))
                return redirect('registro')

            if not re.match(r'^[a-zA-Z\s-]+$', nombre):
                messages.error(request, _("El nombre deben ser sólo letras"))
                return redirect('registro')
            
            if not re.match(r'^[a-zA-Z\s-]+$', apellidos):
                messages.error(request, _("Los apellidos deben ser sólo letras"))
                return redirect('registro')

            if password1 != password2:
                messages.error(request, _("Las contraseñas no coinciden"))
                return redirect('registro')
            
            if User.objects.filter(username=usuario).exists():
                messages.error(request, _("Nombre de usuario ya existe"))
                return redirect('registro')
            
            if User.objects.filter(email=correo).exists():
                messages.error(request, _("Ya existe una cuenta con ese correo"))
                return redirect('registro')

            user = User.objects.create_user(username=usuario,password=password1)
            user.first_name = nombre
            user.last_name = apellidos
            user.email = correo
            user.save()
            login(request,user)

            messages.success(request, _("Registro Exitoso, por favor inicie sesion"))
            return redirect('iniciosesion')
        
        except IntegrityError:  
            messages.error(request, _("Error al registrar usuario. Por favor, inténtelo de nuevo."))
            return redirect('registro')
    
    return render(request, 'registration/registro.html')

def iniciosesion(request):

    if request.method == 'POST':
        try:       
            usuario = request.POST.get('username')
            password1 = request.POST.get('password')

            if not (usuario and password1):
                messages.error(request, _("Debe llenar los campos indicados"))
                return render(request,'app/login.html')

            user = authenticate(request,username=usuario,password=password1)

            if user is not None:
                login(request,user)
                messages.success(request, _("Inicio de sesión correcta"))

                #Valida si el user es superusuario:
                if user.is_superuser:
                    name = request.user.first_name
                    return render(request, 'administrador/administrador_home.html', {'nameadmin':name})
                else:
                    name = request.user.first_name
                    return render(request,'app/home.html', {'name':name})
            else:
                messages.error(request, _("Usuario o contraseña no es correcta"))
                return render(request, 'app/login.html')
            
        except Exception as e:
            messages.error(request, _("Error al iniciar sesión. Por favor, inténtelo de nuevo."))
            return render(request, 'app/login.html')

    return render(request, 'app/login.html')

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect('home')

# Vistas Relacionadas con el usuario registrado:

@login_required
def misreservas(request):
    return render(request, 'registration/mireserva.html')

@login_required
def misdatos(request):
    return render(request, 'registration/datopersonal.html')


# Vista Home
def home(request):
    return render(request,'app/home.html')


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

# VISTAS DEL ADMINISTRADOR

# Vista Administrador Home
@admin_required
def administrador_home(request):
    return render(request, 'administrador/administrador_home.html')

# Vista Administrador Gestion Habitaciones
@admin_required
def gestion_habitaciones(request):
    return render(request, 'administrador/gestion_habitaciones.html')

# Vista Administrador Gestion Habitaciones -crear
@admin_required
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
        messages.success(request, _('¡La habitación se creó exitosamente!'))
    return render(request, 'administrador/gestion_habitaciones/crear_habitacion.html')


# Vista Administrador Gestion Habitaciones-eliminar
@admin_required
def eliminar_habitacion(request):
    if request.method == 'POST':
        id_hab = request.POST.get('id_hab')
        habitacion = Habitacion.objects.get(id_hab=id_hab)
        habitacion.delete()
    # Se obtienen todos los registros de habitaciones
    habitaciones = Habitacion.objects.all()

    return render(request, 'administrador/gestion_habitaciones/eliminar_habitacion.html', {'habitaciones': habitaciones})

# Vista Administrador Gestion Habitaciones-modificar
@admin_required
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
    habitaciones = Habitacion.objects.all()
    return render(request, 'administrador/gestion_habitaciones/modificar_habitacion.html', {'habitaciones': habitaciones})

# Vista Administrador Gestion Habitaciones-ver
@admin_required
def ver_habitacion(request):
    habitaciones = Habitacion.objects.all()

    return render(request, 'administrador/gestion_habitaciones/ver_habitacion.html',{'habitaciones':habitaciones})

# Vista Administrador Gestion Reservas
@admin_required
def gestion_reservas(request):
    return render(request, 'administrador/gestion_reservas.html')

# Vista Administrador Gestion Reservas -crear
@admin_required
def crear_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/crear_reserva_pacific.html')

# Vista Administrador Gestion Reservas -eliminar
@admin_required
def eliminar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/eliminar_reserva_pacific.html')

# Vista Administrador Gestion Reservas -modificar
@admin_required
def modificar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/modificar_reserva_pacific.html')

# Vista Administrador Gestion Reservas -ver calendario
@admin_required
def ver_calendario_pacific(request):
    return render(request, 'administrador/gestion_reservas/ver_calendario_pacific.html')

# Vista Administrador Gestion Reservas -ver reserva
@admin_required
def ver_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/ver_reserva_pacific.html')

# Vista Administrador Gestion Usuarios
@admin_required
def gestion_usuarios(request):
    return render(request, 'administrador/gestion_usuarios.html')

@admin_required
def ver_usuarios_admin(request):
    # Llamo al procedimiento creado en mysql (el cuál está en la línea 432)
    with connection.cursor() as c:
        c.callproc('obtener_todos_usuarios')
        resultado = c.fetchall()
        #creo una lista vacia para almacenar "resultado":
        usuarios = []
        for row in resultado:
            user_result = {}
            for i, column in enumerate(c.description):
                column_name = column[0]
                #Utilizar índice entero para acceder a elementos de una tupla
                column_value = row[i] 
                user_result[column_name] = column_value
            usuarios.append(user_result)

    success_message = request.GET.get('success_message')
    return render(request, 'administrador/gestion_usuarios/ver_usuario.html', 
                  {'usuarios': usuarios, 'success_message': success_message})

def eliminar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        success_message = _("Usuario eliminado con éxito")
        #encoded_success_message = urlencode({'success_message': success_message})
        return HttpResponseRedirect(reverse('ver_usuarios_admin') + f'?{success_message}')

    return render(request, 'administrador/gestion_usuarios/eliminar_usuario.html', {'usuario': usuario})

@admin_required
def crear_usuario_admin(request):
    if request.method == 'POST':
        nombre = request.POST['nombres']
        apellido = request.POST['apellidos']
        usuario = request.POST['nombreusuario']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        password1 = request.POST['contrasena1']
        password2 = request.POST['contrasena2']
        is_superuser = request.POST.get('superusuario', False)

        if not (nombre and apellido and usuario and correo and telefono and password1 and password2):
            messages.error(request, _("Debes llenar todos los campos"))
            return redirect('crear_usuario_admin')
        
        if not re.match(r'^[a-zA-Z\s-]+$', nombre):
            messages.error(request, _("El nombre deben ser sólo letras"))
            return redirect('crear_usuario_admin')
            
        if not re.match(r'^[a-zA-Z\s-]+$', apellido):
            messages.error(request, _("Los apellidos deben ser sólo letras"))
            return redirect('crear_usuario_admin')

        if password1 != password2:
            messages.error(request, _("Las contraseñas no coinciden"))
            return redirect('crear_usuario_admin')
        
        if User.objects.filter(username=usuario).exists():
            messages.error(request, _("Nombre de usuario ya existe"))
            return redirect('crear_usuario_admin')

        if User.objects.filter(email=correo).exists():
            messages.error(request, _("El correo ya es usado por otro usuario"))
            return redirect('crear_usuario_admin')
        
        user = User.objects.create_user(username=usuario,password=password1)
        user.first_name = nombre
        user.last_name = apellido
        user.email = correo
        user.is_superuser = bool(is_superuser)
        user.save()

        messages.success(request, _("Usuario creado con exito"))
        return redirect('ver_usuarios_admin')
    
    return render(request, 'administrador/gestion_usuarios/crear_usuario.html')


@admin_required
def modificar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        nombre = request.POST['nombres']
        apellido = request.POST['apellidos']
        username = request.POST['nombreusuario']
        email = request.POST['correo']
        is_superuser = request.POST.get('superusuario',False)

        if not (nombre and apellido and username and email):
            messages.error(request, _("Debes llenar todos los campos"))
            return redirect('modificar_usuario_admin', id_usuario=id_usuario)
        
        if not re.match(r'^[a-zA-Z\s-]+$', nombre):
            messages.error(request, _("El nombre deben ser sólo letras"))
            return redirect('modificar_usuario_admin', id_usuario=id_usuario)
            
        if not re.match(r'^[a-zA-Z\s-]+$', apellido):
            messages.error(request, _("Los apellidos deben ser sólo letras"))
            return redirect('modificar_usuario_admin', id_usuario=id_usuario)

        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.username = username
        usuario.email = email
        usuario.is_superuser = bool(is_superuser)
        usuario.save()

        success_message = _("Usuario modificado con éxito")
        encoded = urlencode({'success_message': success_message}) # Sin esta linea no se ve los mensajes
        return HttpResponseRedirect(reverse('ver_usuarios_admin') + f'?{encoded}')
    
    return render(request, 'administrador/gestion_usuarios/modificar_usuario.html', {'usuario': usuario})

@admin_required
def cerrarsesionadmin(request):
    logout(request)
    return redirect('home')

# @admin_required
# def modificar_usuario_admin(request, id_usuario):
#     usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario) 
#     if request.method == 'POST':
#         form = RegistroUsuarioAdminForm(request.POST, instance=usuario)
#         if form.is_valid():
#             form.save()
#             return redirect('ver_usuarios_admin')
#     else:
#         form = RegistroUsuarioAdminForm(instance=usuario)
#     return render(request, 'administrador/gestion_usuarios/modificar_usuario.html', {'form': form})

# @admin_required
# def eliminar_usuario_admin(request, id_usuario):
#     usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario)
#     if request.method == 'POST':
#         usuario.delete()
#         return redirect('ver_usuarios_admin')
#     return render(request, 'administrador/gestion_usuarios/eliminar_usuario.html', {'usuario': usuario})


# DROP PROCEDURE IF EXISTS obtener_todos_usuarios;
# DELIMITER $
# CREATE PROCEDURE obtener_todos_usuarios()
# BEGIN
# 	SELECT * FROM auth_user;
# END $
# DELIMITER ;
# CALL obtener_todos_usuarios();

