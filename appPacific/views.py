from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import RegistroUsuario, TipoUsuario, Reserva, ReporteReserva, Habitacion, TipoHabitacion
from django.http import HttpResponse
from .forms import RegistroUsuarioAdminForm
import binascii
import requests
from django.conf import settings
import json
from django.http import JsonResponse
import base64
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.translation import activate
from django.db.models import F

from appPacific import models


# Create your views here.

# Vista Index
def index(request):
    if request.method == 'POST':
        # Input Buscador
        fecha_llegada = request.POST.get('fecha_llegada') or request.GET.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida') or request.GET.get('fecha_salida')
        contador_adultos = int(request.POST.get('contador_adultos', 0)) or int(request.GET.get('contador_adultos', 0))
        contador_ninos = int(request.POST.get('contador_ninos', 0)) or int(request.GET.get('contador_ninos', 0))

        # Guardar datos de búsqueda en la sesión
        request.session['fecha_llegada'] = fecha_llegada
        request.session['fecha_salida'] = fecha_salida
        request.session['contador_adultos'] = contador_adultos
        request.session['contador_ninos'] = contador_ninos
        
        # Redirigir a la vista 'habitaciones'
        return redirect('habitaciones')
    
    idioma = request.LANGUAGE_CODE

    # Obtener todas las habitaciones
    habitaciones = Habitacion.objects.all()

    for habitacion in habitaciones:
        if idioma == 'en':
            habitacion.titulo = habitacion.titulo_en
            habitacion.descripcion = habitacion.descripcion_en
    
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
                messages.error(request, "Por favor, complete todos los campos.")
                return redirect('registro')

            if not (nombre.isalpha()):
                messages.error(request, "El nombre deben ser sólo letras")
                return redirect('registro')
            
            if not (apellidos.isalpha()):
                messages.error(request, "Los apellidos deben ser sólo letras")
                return redirect('registro')

            if password1 != password2:
                messages.error(request, "Las contraseñas no coinciden")
                return redirect('registro')
            
            if User.objects.filter(username=usuario).exists():
                messages.error(request, "Nombre de usuario ya existe")
                return redirect('registro')
            
            if User.objects.filter(email=correo).exists():
                messages.error(request, "Ya existe una cuenta con ese correo")
                return redirect('registro')

            user = User.objects.create_user(username=usuario,password=password1)
            user.first_name = nombre
            user.last_name = apellidos
            user.save()
            login(request,user)

            messages.success(request, "Registro Exitoso, por favor inicie sesion")
            return redirect('iniciosesion')
        
        except IntegrityError:  
            messages.error(request, "Error al registrar usuario. Por favor, inténtelo de nuevo.")
            return redirect('registro')
    
    # return render(request, 'registration/registro.html')
    return render(request, 'registration/registro.html')

def iniciosesion(request):

    if request.method == 'POST':
        try:       
            usuario = request.POST.get('username')
            password1 = request.POST.get('password')

            if not (usuario and password1):
                messages.error(request,"Debe llenar los campos indicados")
                return render(request,'app/login.html')

            user = authenticate(request,username=usuario,password=password1)

            if user is not None:
                login(request,user)
                messages.success(request,"Inicio de sesión correcta")
                name = request.user.first_name
                # Obtener habitaciones
                habitaciones = Habitacion.objects.all()
                return render(request,'app/index.html',{'name':name, 'habitaciones': habitaciones})
            else:
                messages.error(request,"Usuario o contraseña no es correcta")
                return render(request, 'app/login.html')
            
        except Exception as e:
            messages.error(request, "Error al iniciar sesión. Por favor, inténtelo de nuevo.")
            return render(request, 'app/login.html')

    return render(request, 'app/login.html')

@login_required
def cerrarsesion(request):
    logout(request)
    return redirect('index')

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
    # Obtener los parámetros de la URL
    fecha_llegada = request.session.get('fecha_llegada')
    fecha_salida = request.session.get('fecha_salida')
    contador_adultos = request.session.get('contador_adultos')
    contador_ninos = request.session.get('contador_ninos')
    print(fecha_llegada)
    print(fecha_salida)
    print(contador_adultos)
    print(contador_ninos)

    if request.method == 'POST':
        if fecha_llegada and fecha_salida and contador_adultos > 0:
            return render(request, 'app/metodo_pago.html')
        else:
            # Datos de búsqueda incompletos, mostrar mensaje de error o redireccionar a otra vista
            return HttpResponse("Datos de búsqueda incompletos. Por favor, vuelva atrás y complete todos los campos.")

    idioma = request.LANGUAGE_CODE

    # Obtener todas las habitaciones
    habitaciones = Habitacion.objects.all()

    for habitacion in habitaciones:
        if idioma == 'en':
            habitacion.titulo = habitacion.titulo_en
            habitacion.descripcion = habitacion.descripcion_en
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
        titulo_en = request.POST.get('titulo_en')
        descripcion_en = request.POST.get('descripcion_en')
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
            titulo_en=titulo_en,
            descripcion_en=descripcion_en,
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
    paginator = Paginator(habitaciones, 2)  # Número de habitaciones por página
    num_pages = paginator.num_pages
    page_range = range(1, num_pages + 1)
    return render(request, 'administrador/gestion_habitaciones/ver_habitacion.html', {'habitaciones': habitaciones, 'page_range': page_range})


# Vista Administrador Gestion Reservas
def gestion_reservas(request):
    return render(request, 'administrador/gestion_reservas.html')

# Vista Administrador Gestion Reservas -crear
def crear_reserva_pacific(request):
    reservas = Reserva
    if request.method == 'POST':
        id_reserva = request.POST.get('id_reserva')
        nombre_cli = request.POST.get('nombre_cli')
        apellidos_cli = request.POST.get('apellidos_cli')
        rut_cli = request.POST.get('rut_cli')
        metodo_pago = request.POST.get('metodo_pago')
        pago_reserva = request.POST.get('pago_reserva')
        total_restante = request.POST.get('total_restante')
        estado_pago = request.POST.get('estado_pago')

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
def crear_usuario_admin(request):
    if request.method == 'POST':
        form = RegistroUsuarioAdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_usuarios_admin')
    else:
        form = RegistroUsuarioAdminForm()

    return render(request, 'administrador/gestion_usuarios/crear_usuario.html', {'form': form})

# Vista Administrador Gestion Usuarios -ver usuario
def ver_usuarios_admin(request):
    usuarios = RegistroUsuario.objects.all()
    return render(request, 'administrador/gestion_usuarios/ver_usuario.html', {'usuarios': usuarios})


# Vista Administrador Gestion Usuarios modificar usuario
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

# Vista Administrador Gestion Usuarios -eliminar usuario
def eliminar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario)
    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuarios_admin')
    return render(request, 'administrador/gestion_usuarios/eliminar_usuario.html', {'usuario': usuario})

# Vista Administrador Gestion Usuarios -tipo de usuario
def tipo_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(RegistroUsuario, id_user=id_usuario)
    if request.method == 'POST':
        nuevo_rol = request.POST.get('rol')  
        usuario.rol = nuevo_rol
        usuario.save()
        return redirect('ver_usuarios_admin')
    else:
        return render(request, 'administrador/gestion_usuarios/tipo_usuario_admin.html', {'usuario': usuario})
    



# Vistas PAYPAL
@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart')

        access_token = generate_access_token()

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": "100.00"  # You may need to calculate this from the cart
                    }
                }
            ]
        }

        response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            },
            json=payload
        )

        return handle_response(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_POST
def capture_order(request, order_id):
    try:
        access_token = generate_access_token()

        response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )

        return handle_response(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generate_access_token():
    try:
        if not (settings.PAYPAL_CLIENT_ID and settings.PAYPAL_CLIENT_SECRET):
            raise Exception("MISSING_API_CREDENTIALS")

        auth = base64.b64encode(
            f"{settings.PAYPAL_CLIENT_ID}:{settings.PAYPAL_CLIENT_SECRET}".encode()
        ).decode()

        response = requests.post(
            f"{settings.PAYPAL_BASE_URL}/v1/oauth2/token",
            data={"grant_type": "client_credentials"},
            headers={"Authorization": f"Basic {auth}"}
        )

        data = response.json()
        return data.get("access_token")

    except Exception as e:
        raise Exception(f"Failed to generate Access Token: {str(e)}")


def handle_response(response):
    try:
        response_data = response.json()
        return JsonResponse(response_data, status=response.status_code)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)