from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from appPacific.decorators import admin_required
from .models import RegistroUsuario, TipoUsuario, Reserva, ReporteReserva, Habitacion, TipoHabitacion, DatosBancarios
from django.http import HttpResponse, HttpResponseRedirect
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
import random
import string
from django.contrib.sessions.models import Session
import re
from appPacific import models
import re
from django.utils.translation import gettext as _
from .decorators import admin_required
from urllib.parse import urlencode
from django.db import connection

# Create your views here.

# Vista Index
def index(request):
    if request.method == 'POST':
        # Input Buscador
        fecha_llegada = request.POST.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida')
        fecha_llegada_formateada = request.POST.get('fecha_llegada_hidden')
        fecha_salida_formateada = request.POST.get('fecha_salida_hidden')
        contador_adultos = int(request.POST.get('contador_adultos', 0))
        contador_ninos_str = request.POST.get('contador_ninos')
        contador_ninos = int(contador_ninos_str) if contador_ninos_str else 0

        # Validar que los campos de fechas no estén vacíos
        if not fecha_llegada or not fecha_salida:
            messages.error(request, "Por favor, completa las fechas de llegada y salida")
            return redirect('index')

        # Guardar datos de búsqueda en la sesión
        request.session['fecha_llegada'] = fecha_llegada
        request.session['fecha_salida'] = fecha_salida
        # Fechas formateadas
        request.session['fecha_llegada_hidden'] = fecha_llegada_formateada
        request.session['fecha_salida_hidden'] = fecha_salida_formateada
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
                messages.error(request, _("Por favor, complete todos los campos."))
                return redirect('registro')

            if not re.match(r'^[a-zA-Z\s-]+$', nombre):
                messages.error(request, _("El nombre deben ser sólo letras"))
            if not re.match(r'^[a-zA-Z\s-]+$', nombre):
                messages.error(request, "El nombre deben ser sólo letras")
                return redirect('registro')
            
            if not re.match(r'^[a-zA-Z\s-]+$', apellidos):
                messages.error(request, _("Los apellidos deben ser sólo letras"))
            if not re.match(r'^[a-zA-Z\s-]+$', apellidos):
                messages.error(request, "Los apellidos deben ser sólo letras")
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

            messages.success(request, "Registro Exitoso, por favor inicie sesion")
            return redirect('index')
        
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
                messages.success(request,"Inicio de sesión correcta")
                name = request.user.first_name
                request.session['id_user'] = user.id

                # messages.success(request, _("Inicio de sesión correcta"))
                
                #Valida si el user es superusuario:
                if user.is_superuser:
                    name = request.user.first_name
                    return render(request, 'administrador/administrador_home.html', {'nameadmin':name})
                else:
                    name = request.user.first_name
                    return render(request,'app/index.html', {'name':name})
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
    # Obtener los parámetros de la URL
    fecha_llegada = request.session.get('fecha_llegada')
    fecha_salida = request.session.get('fecha_salida')
    contador_adultos = request.session.get('contador_adultos')
    contador_ninos = request.session.get('contador_ninos')

    if request.method == 'POST' and fecha_llegada and fecha_salida and contador_adultos > 0:
        # Obtener los id de la habitacion cuando se haga clic en botón Reserva
        id_hab = int(request.POST.get('id_hab'))
        id_tipo_hab = request.POST.get('id_tipo_hab')

        row_hab = Habitacion.objects.get(id_hab=id_hab)
        row_tipo_hab = TipoHabitacion.objects.get(id_tipo_hab=id_tipo_hab)

        # Guardar los id de ambas habitaciones en sesiones
        request.session['id_hab'] = row_hab.id_hab
        request.session['tipo_hab'] = row_tipo_hab.tipo_hab
        request.session['precio'] = row_hab.precio

        return redirect('metodo_pago')

    idioma = request.LANGUAGE_CODE
    habitaciones = Habitacion.objects.all()
    for habitacion in habitaciones:
        if idioma == 'en':
            habitacion.titulo = habitacion.titulo_en
            habitacion.descripcion = habitacion.descripcion_en
    return render(request, 'app/habitaciones.html', {'habitaciones': habitaciones})

# Vista Método Pago
def metodo_pago(request):
    # Obtener los parámetros para mostrar en vista de método de pago
    fecha_llegada = request.session.get('fecha_llegada')
    fecha_salida = request.session.get('fecha_salida')
    contador_adultos = request.session.get('contador_adultos')
    contador_ninos = request.session.get('contador_ninos')

    # Obtener valores de id_hab y id_tipo_hab
    id_hab = request.session.get('id_hab')
    tipo_hab = request.session.get('tipo_hab')

    # Obtener precio de habitacion
    row_hab = Habitacion.objects.get(pk=id_hab)
    precio = row_hab.precio

    precio_int = int(row_hab.precio)
    print("El precio en vista de metodo_pago es: ", precio)

    # Calcular 30% del total
    pago_inicial = int(0.3*precio_int)
    pago_pendiente = int(0.7*precio_int)

    # Guardar en una session los datos de total, pago_inicial, pago_pendiente
    request.session['total'] = precio_int
    request.session['pago_inicial'] = pago_inicial
    request.session['pago_pendiente'] = pago_pendiente

    # Crear obteto cuando se selecciona habitacion
    hab_seleccionada = {
        'tipo_hab': tipo_hab,
        'fecha_llegada': fecha_llegada,
        'fecha_salida': fecha_salida,
        'contador_adultos': contador_adultos,
        'contador_ninos': contador_ninos,
        'total': precio_int,
        'pago_inicial': pago_inicial,
        'pago_pendiente': pago_pendiente
    }

    return render(request, 'app/metodo_pago.html', {'hab_seleccionada':hab_seleccionada})


def generar_codigo(length=8):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(length))
    return codigo

def obtener_o_generar_codigo(request):
    if 'codigo_referencia' in request.session:
        # Si ya hay un código almacenado en la sesión, lo devuelve
        codigo_referencia = request.session['codigo_referencia']
    else:
        # Si no hay un código almacenado en la sesión, genera uno nuevo
        codigo_referencia = generar_codigo()
        # Almacena el código en la sesión para futuras solicitudes
        request.session['codigo_referencia'] = codigo_referencia
    return codigo_referencia


# Vista Transferencia Bancaria
def transferencias(request):
    datos_bancarios = DatosBancarios.objects.get(pk=1)
    beneficiario = datos_bancarios.beneficiario
    cuenta = datos_bancarios.cuenta
    nro_cuenta = datos_bancarios.nro_cuenta
    correo_banco = datos_bancarios.correo_banco
    pago_inicial = request.session.get('pago_inicial')
    id_reserva = request.session.get('id_reserva')

    codigo_referencia = obtener_o_generar_codigo(request)

    datos = {
        'beneficiario': beneficiario,
        'cuenta': cuenta, 
        'nro_cuenta': nro_cuenta,
        'correo_banco': correo_banco,
        'pago_inicial': pago_inicial,
        'codigo_referencia': codigo_referencia
    }

    id_user = request.session.get('id_user')
    # Obtener fecha_llegada
    fecha_llegada = request.session.get('fecha_llegada')
    # Obtener fecha_salida
    fecha_salida = request.session.get('fecha_salida')
    # Obtener cant_adultos
    cant_adultos = request.session.get('contador_adultos')
    # Obtener cant_ninos
    cant_ninos = request.session.get('contador_ninos')
    # Tipo de pago por transferencia bancaria
    tipo_metodo_pago = 'Transferencia Bancaria'
    # Obtener total de la reserva
    total = request.session.get('total')
    # Obtener mediante session el pago_pendiente de la reserva
    pago_pendiente = request.session.get('pago_pendiente')

    # Fechas formateadas
    fecha_llegada_formateada = request.session.get('fecha_llegada_hidden')
    fecha_salida_formateada = request.session.get('fecha_salida_hidden')

    return render(request, 'app/transferencias.html', {'datos': datos})

# Vista Reserva Realizada
def reserva_realizada(request):
    id_user = request.session.get('id_user')
    datos_usuario = User.objects.get(pk = id_user)

    # Obtener el Order ID de PayPal
    order_id = request.session.get('order_id')

    datos_reserva = Reserva.objects.get(id_user = id_user, order_id = order_id)
    return render(request, 'app/reserva_realizada.html', {'datos_reserva': datos_reserva, 'datos_usuario': datos_usuario})

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
        messages.success(request, _('¡La habitación se creó exitosamente!'))
    return render(request, 'administrador/gestion_habitaciones/crear_habitacion.html')


# Vista Administrador Gestion Habitaciones-eliminar
@admin_required
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
    paginator = Paginator(habitaciones, 2)  # Número de habitaciones por página
    num_pages = paginator.num_pages
    page_range = range(1, num_pages + 1)
    return render(request, 'administrador/gestion_habitaciones/ver_habitacion.html', {'habitaciones': habitaciones, 'page_range': page_range})


# Vista Administrador Gestion Reservas
@admin_required
def gestion_reservas(request):
    return render(request, 'administrador/gestion_reservas.html')

# Vista Administrador Gestion Reservas -crear
@admin_required
def crear_reserva_pacific(request):
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
@admin_required
def eliminar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/eliminar_reserva_pacific.html')

# Vista Administrador Gestion Reservas -modificar
@admin_required
def modificar_reserva_pacific(request):
    return render(request, 'administrador/gestion_reservas/modificar_reserva_pacific.html')

@admin_required
def modificar_reporte_reserva(request):
    # Ingresar en buscador el id_reserva para filtrar los reportes
    id_reserva = requests.POST.get('id_reserva')
    reporte_reserva = ReporteReserva.objects.get(pk=id_reserva)
    if request.method == 'POST':
        reporte_reserva.hacer_checkin(hora_ingreso=datetime.now().time()) 
        reporte_reserva.hacer_checkout(hora_salida=datetime.now().time()) 
    return render(request, 'administrador/gestion_reservas/modificar_reporte_reserva.html')

# Vista Administrador Gestion Reservas -ver calendario
@admin_required
def ver_calendario_pacific(request):
    return render(request, 'administrador/gestion_reservas/ver_calendario_pacific.html')

# Vista Administrador Gestion Reservas -ver reserva
@admin_required
def ver_reserva_pacific(request):
    reservas = Reserva.objects.all()
    return render(request, 'administrador/gestion_reservas/ver_reserva_pacific.html', {'reservas': reservas})

# Vista Administrador Gestion Usuarios
@admin_required
def gestion_usuarios(request):
    return render(request, 'administrador/gestion_usuarios.html')

# Vista Administrador Gestion Usuarios -crear usuario
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

# Vista Administrador Gestion Usuarios -ver usuario
@admin_required
def ver_usuarios_admin(request):
    usuarios = RegistroUsuario.objects.all()
    return render(request, 'administrador/gestion_usuarios/ver_usuario.html', {'usuarios': usuarios})


# Vista Administrador Gestion Usuarios modificar usuario
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

# Vista Administrador Gestion Usuarios -eliminar usuario
@admin_required
def eliminar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
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

        # Obtener Precio de Habitacion Seleccionada
        pago_inicial = request.session.get('pago_inicial')

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(pago_inicial)
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
        response_data = response.json()
        # Guardar el Order Id de Paypal
        request.session['order_id'] = order_id

        # Verificar si la captura fue exitosa
        if response.status_code == 201 and response_data.get('status') == 'COMPLETED':
            # Obtener Id de la Habitacion
            id_hab = request.session.get('id_hab')
            # Obtener Id Usuario
            id_user = request.session.get('id_user')
            print("ID usuario logeado: ", id_user)

            # Obtener Order ID de Paypal
            order_id = request.session.get('order_id')
            print("Order ID: ", order_id)

            # Obtener fecha_llegada
            fecha_llegada = request.session.get('fecha_llegada')
            # Obtener fecha_salida
            fecha_salida = request.session.get('fecha_salida')
            # Obtener cant_adultos
            cant_adultos = request.session.get('contador_adultos')
            # Obtener cant_ninos
            cant_ninos = request.session.get('contador_ninos')
            tipo_hab = request.session.get('tipo_hab')
            tipo_metodo_pago = 'PayPal'
            # Obtener total
            total = request.session.get('total')
            # Con el Id de la habitacion obtener el registro de datos
            row_hab = Habitacion.objects.get(pk=id_hab)
            # Mediante session obtener el pago_inicial de la reserva
            pago_inicial = request.session.get('pago_inicial')
            # Obtener mediante session el pago_pendiente de la reserva
            pago_pendiente = request.session.get('pago_pendiente')

            # Fechas formateadas
            fecha_llegada_formateada = request.session.get('fecha_llegada_hidden')
            fecha_salida_formateada = request.session.get('fecha_salida_hidden')

            # Crear objeto Reserva
            reserva = Reserva(
                id_user = id_user,
                order_id = order_id,
                fecha_llegada = fecha_llegada_formateada,
                fecha_salida = fecha_salida_formateada,
                cant_adultos = cant_adultos,
                cant_ninos = cant_ninos,
                tipo_hab = tipo_hab,
                tipo_metodo_pago = tipo_metodo_pago,
                total = total,
                pago_inicial = pago_inicial,
                pago_pendiente = pago_pendiente,
            )
            # Crear Reporte Reserva
            reporte_reserva = ReporteReserva(
                dia_ingreso = fecha_llegada_formateada,
                dia_salida = fecha_salida_formateada
            )
            # Guardar objeto Reserva y Reporte Reserva en la base de datos
            reserva.save()
            reporte_reserva.save()

        else:
            return JsonResponse(response_data, status=response.status_code)

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

@admin_required
def cerrarsesionadmin(request):
    logout(request)
    return redirect('index')



@admin_required
def cerrarsesionadmin(request):
    logout(request)
    return redirect('home')
    

# DROP PROCEDURE IF EXISTS obtener_todos_usuarios;
# DELIMITER $
# CREATE PROCEDURE obtener_todos_usuarios()
# BEGIN
# 	SELECT * FROM auth_user;
# END $
# DELIMITER ;
# CALL obtener_todos_usuarios();   
    

# Vista Vendedor Home
def vendedor_home(request):
    return render(request, 'vendedor/vendedor_home.html')

# Vista Vendedor Gestion Reservas
def gestion_reservas_vendedor(request):
    return render(request, 'vendedor/gestion_reservas_vendedor.html')

# Vista Vendedor Gestion Reservas -crear
def crear_reserva_pacific_vendedor(request):
    if request.method == 'POST':
        id_reserva = request.POST.get('id_reserva')
        nombre_cli = request.POST.get('nombre_cli')
        apellidos_cli = request.POST.get('apellidos_cli')
        rut_cli = request.POST.get('rut_cli')
        metodo_pago = request.POST.get('metodo_pago')
        pago_reserva = request.POST.get('pago_reserva')
        total_restante = request.POST.get('total_restante')
        estado_pago = request.POST.get('estado_pago')

    return render(request, 'vendedor/gestion_reservas_vendedor/crear_reserva_pacific_vendedor.html')

# Vista Vendedor Gestion Reservas -eliminar
def eliminar_reserva_pacific_vendedor(request):
    return render(request, 'vendedor/gestion_reservas_vendedor/eliminar_reserva_pacific_vendedor.html')

# Vista Vendedor Gestion Reservas -modificar
def modificar_reserva_pacific_vendedor(request):
    return render(request, 'vendedor/gestion_reservas_vendedor/modificar_reserva_pacific_vendedor.html')

# Vista Vendedor Gestion Reservas -ver calendario
def ver_calendario_pacific_vendedor(request):
    return render(request, 'vendedor/gestion_reservas_vendedor/ver_calendario_pacific_vendedor.html')

# Vista Vendedor Gestion Reservas -ver reserva
def ver_reserva_pacific_vendedor(request):
    return render(request, 'vendedor/gestion_reservas_vendedor/ver_reserva_pacific_vendedor.html')