import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from appPacific.decorators import admin_required
from .models import RegistroUsuario, TipoUsuario, Reserva, ReporteReserva, Habitacion, TipoHabitacion, DatosBancarios, MetodoPago
from django.http import HttpResponse, HttpResponseRedirect
import binascii
import locale
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
from datetime import datetime, timedelta
from appPacific import models
from django.utils.translation import gettext as _
from .decorators import admin_required, seller_required
from django.db import connection
from django.shortcuts import render
from django.views.generic import View
from rest_framework import generics
from .serializers import MetodoPagoSerializer, ReservaSerializer, ReporteReservaSerializer, TipoHabitacionSerializer, HabitacionSerializer, DatosBancariosSerializer
import calendar
from django.contrib.auth.models import AnonymousUser

# Create your views here.

# Vista Index
def index(request):
    habitacion_visible = request.POST.get('id_hab')
    print(habitacion_visible)

    if request.method == 'POST':
        # Input Buscador
        fecha_llegada = request.POST.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida')
        fecha_llegada_formateada = request.POST.get('fecha_llegada_hidden')
        fecha_salida_formateada = request.POST.get('fecha_salida_hidden')
        contador_adultos = int(request.POST.get('contador_adultos', 0))
        contador_ninos_str = request.POST.get('contador_ninos')
        contador_ninos = int(contador_ninos_str) if contador_ninos_str else 0
        total_huespedes = contador_adultos + contador_ninos # Contar Adultos y niños
        total_huespedes_str = str(total_huespedes)

        # Validar que los campos de fechas no estén vacíos
        if fecha_llegada is None or fecha_salida is None or contador_adultos == 0:
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
        request.session['total_huespedes_str'] = total_huespedes_str
        
        # Redirigir a la vista 'habitaciones'
        return redirect('habitaciones')
    
    idioma = request.LANGUAGE_CODE
    # Obtener todas las habitaciones
    habitaciones = Habitacion.objects.all()

    for habitacion in habitaciones:
        if idioma == 'en':
            habitacion.titulo_hab = habitacion.titulo_en
            habitacion.descripcion = habitacion.descripcion_en
    
    return render(request, 'app/index.html', {'habitaciones': habitaciones, 'habitacion_visible':habitacion_visible})

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

            # messages.success(request, "Registro Exitoso, por favor inicie sesion")
            return redirect('index')
        
        except IntegrityError:  
            messages.error(request, _("Error al registrar usuario. Por favor, inténtelo de nuevo."))
            return redirect('registro')
    
    return render(request, 'registration/registro.html')

def iniciosesion(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('administrador_home')
        else:
            return redirect('index')

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
                # messages.success(request,"Inicio de sesión correcta")
                name = request.user.first_name
                request.session['id_user'] = user.id
                # messages.success(request, _("Inicio de sesión correcta"))
                
                #Valida si el user es superusuario:
                if user.is_superuser:
                    return redirect('administrador_home')
                else:
                    return redirect('index')
                #Valida si el user es vender:
                if user.is_staff:
                    return redirect('vendedor_home')           
                else:
                    return redirect('home')
                    
            else:
                messages.error(request, _("Usuario o contraseña no es correcta"))
                return render(request, 'app/login.html')
            
        except Exception as e:
            messages.error(request, _("Error al iniciar sesión. Por favor, inténtelo de nuevo."))
            return render(request, 'app/login.html')

    return render(request, 'app/login.html')


@login_required
def cerrarsesion(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return redirect('iniciosesion')

# Vistas Relacionadas con el usuario registrado:
@login_required
def misreservas(request):
    id_user = request.session.get('id_user')
    reservas = Reserva.objects.filter(id_user = id_user)
    print(reservas)
    return render(request, 'registration/misreservas.html',{'reservas': reservas})

@login_required
def misdatos(request):
    id_user = request.session.get('id_user')
    datos_usuario = User.objects.get(pk = id_user)
    return render(request, 'registration/datopersonal.html',{'datos_usuario': datos_usuario})

# Vista Home
def home(request):
    if request.user.is_authenticated:
        name = request.user.first_name
    else:
        name = None
    return render(request,'app/home.html', {'name': name})


# Vista Contacto
def contacto(request):
    return render(request, 'app/contacto.html')


# Vista Habitaciones
def habitaciones(request):
    habitaciones = Habitacion.objects.all()
    # Obtener los parámetros de la URL
    fecha_llegada = request.session.get('fecha_llegada')
    fecha_salida = request.session.get('fecha_salida')
    contador_adultos = request.session.get('contador_adultos')
    contador_ninos = request.session.get('contador_ninos')
    total_huespedes_str = request.session.get('total_huespedes_str')

    # Validar si los campos son nulos y redirigir si es necesario
    if fecha_llegada is None or fecha_salida is None or contador_adultos == 0:
        return redirect('index')

    if request.method == 'POST' and fecha_llegada and fecha_salida and contador_adultos > 0:
        # Obtener los id de la habitacion cuando se haga clic en botón Reserva
        id_hab = request.POST.get('id_hab')
        row_hab = Habitacion.objects.get(id_hab=id_hab)
        id_tipo_hab = request.POST.get('id_tipo_hab')
        row_tipo_hab = TipoHabitacion.objects.get(id_tipo_hab=id_tipo_hab)
        capacidad_max = row_hab.capacidad_max
        if int(total_huespedes_str) <= capacidad_max:
            # Guardar los id de ambas habitaciones en sesiones
            request.session['id_hab'] = row_hab.id_hab
            request.session['titulo_hab'] = row_hab.titulo_hab
            request.session['tipo_hab'] = row_tipo_hab.tipo_hab
            request.session['precio'] = row_hab.precio
        else:
            # Mostrar mensaje de que debe ingresar hasta cierta cantidad de huéspedes.
            messages.error(request, _('La cantidad de huéspedes ingresada supera la capacidad permitida.'))
            return render(request, 'app/habitaciones.html', {'habitaciones': habitaciones})

        return redirect('metodo_pago')
    
    idioma = request.LANGUAGE_CODE
    
    for habitacion in habitaciones:
        if idioma == 'en':
            habitacion.titulo_hab = habitacion.titulo_en
            habitacion.descripcion = habitacion.descripcion_en
    return render(request, 'app/habitaciones.html', {'habitaciones': habitaciones})

# Vista Método Pago
def metodo_pago(request):
    # Obtener valores de id_hab y id_tipo_hab
    id_hab = request.session.get('id_hab')
    tipo_hab = request.session.get('tipo_hab')
    # Obtener los parámetros para mostrar en vista de método de pago
    fecha_llegada = request.session.get('fecha_llegada')
    fecha_salida = request.session.get('fecha_salida')
    contador_adultos = request.session.get('contador_adultos')
    contador_ninos = request.session.get('contador_ninos')
    titulo_hab = request.session.get('titulo_hab')

    # Obtener precio de habitacion
    row_hab = Habitacion.objects.get(id_hab=id_hab)
    total = int(row_hab.precio)

    # Calcular 30% del total
    pago_inicial = int(0.3*total)
    pago_pendiente = int(0.7*total)

    # Guardar en una session los datos de total, pago_inicial, pago_pendiente
    request.session['total'] = total
    request.session['pago_inicial'] = pago_inicial
    request.session['pago_pendiente'] = pago_pendiente

    # Crear obteto cuando se selecciona habitacion
    hab_seleccionada = {
        'tipo_hab': tipo_hab,
        'titulo_hab': titulo_hab,
        'fecha_llegada': fecha_llegada,
        'fecha_salida': fecha_salida,
        'contador_adultos': contador_adultos,
        'contador_ninos': contador_ninos,
        'total': total,
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
    id_user = request.session.get('id_user')
    datos_usuario = User.objects.get(pk = id_user)
    nombre_de_usuario = datos_usuario.username
    return render(request, 'administrador/administrador_home.html', {'nameadmin': nombre_de_usuario})

# Vista Administrador Gestion Habitaciones
@admin_required
def gestion_habitaciones(request):
    name = request.user.first_name
    return render(request, 'administrador/gestion_habitaciones.html', {'nameadmin': name})

# Vista Administrador Gestion Habitaciones -crear
@admin_required
def crear_habitacion(request):
    if request.method == 'POST':
        id_tipo_hab = request.POST.get('id_tipo_hab')
        titulo_hab = request.POST.get('titulo_hab')
        descripcion = request.POST.get('descripcion')
        titulo_en = request.POST.get('titulo_en')
        descripcion_en = request.POST.get('descripcion_en')
        capacidad_max = request.POST.get('capacidad_max')
        precio = request.POST.get('precio')
        imagen_bytes = request.FILES.get('cargarImagen').read()

        # Codificar los bytes de la imagen en base64
        imagen_base64 = base64.b64encode(imagen_bytes)
        imagen_base64_str = imagen_base64.decode('utf-8')

        # Buscar el objeto TipoHabitacion con el ID proporcionado (Esto trae Suite, Premium o Twin)
        row_tipo_habitacion = TipoHabitacion.objects.get(id_tipo_hab=id_tipo_hab)

        # Crear la instancia de Habitacion con la imagen codificada en base64
        habitacion = Habitacion(
            id_tipo_hab=row_tipo_habitacion,
            titulo_hab=titulo_hab,
            descripcion=descripcion,
            titulo_en=titulo_en,
            descripcion_en=descripcion_en,
            capacidad_max = capacidad_max,
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
        titulo_hab = request.POST.get('titulo_hab')
        descripcion = request.POST.get('descripcion')
        capacidad_max = request.POST.get('capacidad_max')
        precio = request.POST.get('precio')
        estado = request.POST.get('estado')

        habitacion = Habitacion.objects.get(id_hab=id_hab)
        row_tipo_habitacion = TipoHabitacion.objects.get(id_tipo_hab = id_tipo_hab)

        # Actualizar los campos de la habitación
        habitacion.id_tipo_hab = row_tipo_habitacion
        habitacion.titulo_hab = titulo_hab
        habitacion.descripcion = descripcion
        habitacion.capacidad_max = capacidad_max
        habitacion.precio = precio
        habitacion.estado = estado
        # Guardar actualizaciones de habitación
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
    name = request.user.first_name
    return render(request, 'administrador/gestion_reservas.html', {'nameadmin': name})

# Vista Administrador Gestion Reservas -crear
@admin_required
def crear_reserva_pacific(request):
    # Obtener lista de tipos de habitaciones
    lista_tipo_hab = TipoHabitacion.objects.all()

    if request.method == 'GET' and 'id_tipo_hab' in request.GET:
        id_tipo_hab = request.GET.get('id_tipo_hab')
        hab_disponibles = Habitacion.objects.filter(id_tipo_hab=id_tipo_hab, estado='Disponible').values('id_tipo_hab', 'titulo_hab', 'capacidad_max','precio')
        for habitacion in hab_disponibles:
            id_tipo_hab = habitacion['id_tipo_hab']
            titulo_hab = habitacion['titulo_hab']
            print("La habitacion es: ", titulo_hab)
            capacidad_max = habitacion['capacidad_max']
            precio = int(habitacion['precio'])
            pago_inicial = int(precio*0.3)
            pago_pendiente = int(precio*0.7)
            request.session['titulo_hab'] = titulo_hab
            request.session['precio'] = precio
            request.session['pago_inicial'] = pago_inicial
            request.session['pago_pendiente'] = pago_pendiente
            print(f'ID del tipo de habitación: {id_tipo_hab}, Título de la habitación: {titulo_hab}, Capacidad máxima: {capacidad_max}')
        return JsonResponse({'habitaciones': list(hab_disponibles)})
    
    if request.method == 'POST':
        nombre_cli = request.POST.get('nombre_cli')
        apellidos_cli = request.POST.get('apellidos_cli')
        user = User.objects.get(first_name=nombre_cli, last_name=apellidos_cli)
        id_user = user.id
        correo = request.POST.get('correo')
        celular = request.POST.get('celular')
        fecha_llegada = request.POST.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida')
        cant_adultos = request.POST.get('cant_adultos')
        cant_ninos = request.POST.get('cant_ninos')

        paypal = request.POST.get('paypal')
        get_titulo_hab = request.session.get('titulo_hab')
        print("Titulo habitacion POST: ", get_titulo_hab)
        get_precio = request.session.get('precio')
        get_pago_inicial = request.session.get('pago_inicial')
        get_pago_pendiente = request.session.get('pago_pendiente')

        if paypal:
            reserva = Reserva(
                id_user = id_user,
                fecha_llegada = fecha_llegada,
                fecha_salida = fecha_salida,
                cant_adultos =  cant_adultos,
                cant_ninos =  cant_ninos,
                habitacion = get_titulo_hab, # Se debe cambiar a ID Habitación
                tipo_metodo_pago = paypal,
                total = get_precio,
                pago_inicial = get_pago_inicial,
                pago_pendiente = get_pago_pendiente,
                estado_pago = 'En Espera de Pago'
            )

            row_habitacion = Habitacion.objects.get()
            # Guardar reserva
            reserva.save()
        
        return JsonResponse({'success': True})  # Devuelve una respuesta JSON de éxito

    return render(request, 'administrador/gestion_reservas/crear_reserva_pacific.html', {'lista_tipo_hab': lista_tipo_hab})

# Vista Administrador Gestion Reservas -eliminar
@admin_required
def eliminar_reserva_pacific(request):
    # Se obtienen todos los registros de habitaciones
    reservas = Reserva.objects.all()
    if request.method == 'POST':
        # Obtener el input hidden id_reserva
        id_reserva = request.POST.get('id_reserva')
        # Obtener del input hidden el id_hab de la reserva
        id_hab = request.POST.get('id_hab')
        reserva = get_object_or_404(Reserva, id_reserva=id_reserva)
        reserva.delete()
        messages.success(request, _("Reserva Eliminada Exitosamente"))
        # Cuando se elimine una reserva, cambiar estado de habitación a "Disponible"
        habitacion = Habitacion.objects.get(pk= id_hab)
        # Cambiar estado a "Disponible"
        habitacion.estado = "Disponible"
        # Actualizar el estado en BBDD
        habitacion.save()
    
    return render(request, 'administrador/gestion_reservas/eliminar_reserva_pacific.html',{'reservas': reservas})

# Vista Administrador Gestion Reservas -modificar
@admin_required
def modificar_reserva_pacific(request):
    if request.method == 'POST':
        id_reserva = request.POST.get('id_reserva')
        fecha_llegada = request.POST.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida')

        fecha_llegada_obj = datetime.strptime(fecha_llegada, '%Y-%m-%d').date()
        fecha_salida_obj = datetime.strptime(fecha_salida, '%Y-%m-%d').date()

        cant_adultos = request.POST.get('cant_adultos')
        cant_ninos = request.POST.get('cant_ninos')
        habitacion = request.POST.get('habitacion')
        tipo_metodo_pago = request.POST.get('tipo_metodo_pago')
        estado_pago = request.POST.get('estado_pago')
        
        # Obtener datos de reserva por id_reserva
        reserva = Reserva.objects.get(id_reserva = id_reserva)
        # Actualizar campos de reserva
        reserva.fecha_llegada = fecha_llegada_obj
        reserva.fecha_salida = fecha_salida_obj
        reserva.cant_adultos = cant_adultos
        reserva.cant_ninos = cant_ninos
        reserva.habitacion = habitacion
        reserva.estado_pago = estado_pago
        # Guardar actualizaciones de reserva
        reserva.save()

    reservas = Reserva.objects.all()

    for reserva in reservas:
        reserva.fecha_llegada = reserva.fecha_llegada.strftime('%Y-%m-%d')
        reserva.fecha_salida = reserva.fecha_salida.strftime('%Y-%m-%d')
    
    return render(request, 'administrador/gestion_reservas/modificar_reserva_pacific.html', {'reservas': reservas})

@admin_required
def modificar_reporte_reserva(request):
    # Ingresar en buscador el id_reserva para filtrar los reportes
    id_reserva = requests.POST.get('id_reserva')
    reporte_reserva = ReporteReserva.objects.get(pk=id_reserva)
    if request.method == 'POST':
        reporte_reserva.hacer_checkin(hora_ingreso=datetime.now().time())
        reporte_reserva.hacer_checkout(hora_salida=datetime.now().time())
    return render(request, 'administrador/gestion_reservas/modificar_reporte_reserva.html')

# Obtener fechas calendario
def obtener_dias_mes(mes, año):
    # Obtener el nombre del mes
    nombre_mes = calendar.month_name[mes]
    
    # Obtener el calendario del mes
    calendario_mes = calendar.monthcalendar(año, mes)
    
    # Lista para almacenar los días del mes junto con el nombre del día
    dias_del_mes = []
    
    # Iterar sobre cada semana del calendario del mes
    for semana in calendario_mes:
        for dia in semana:
            # Si el día es diferente de 0, es un día del mes
            if dia != 0:
                # Obtener el nombre del día
                nombre_dia = calendar.day_name[calendar.weekday(año, mes, dia)]
                # Agregar el día y el nombre del día a la lista
                dias_del_mes.append((dia, nombre_dia))
    
    return nombre_mes, dias_del_mes


# Vista Administrador Gestion Reservas -ver calendario
@admin_required
def ver_calendario_pacific(request):
    # Establecer la localización en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener día actual
    dia_actual = datetime.now().day
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    # Obtener los días del mes actual
    nombre_mes_actual, dias_mes_actual = obtener_dias_mes(mes_actual, año_actual)
    nombre_mes_actual = nombre_mes_actual.capitalize()

    lista_dias = ['Lun.', 'Mar.', 'Mié.','Jue.','Vié.','Sáb.','Dom.']

    return render(request, 'administrador/gestion_reservas/ver_calendario_pacific.html', {
        'dia_actual': dia_actual,
        'nombre_mes_actual': nombre_mes_actual,
        'dias_mes_actual': dias_mes_actual,
        'año_actual': año_actual,
        'lista_dias': lista_dias
    })

# Vista Administrador Gestion Reservas -ver reserva
@admin_required
def ver_reserva_pacific(request):
    reservas = Reserva.objects.all()
    return render(request, 'administrador/gestion_reservas/ver_reserva_pacific.html', {'reservas': reservas})

@admin_required
def ver_reporte_pacific(request):
    reporte_reservas = ReporteReserva.objects.all()
    return render(request, 'administrador/gestion_reservas/ver_reporte_pacific.html', {'reporte_reservas': reporte_reservas})

# Vista Administrador Gestion Usuarios
@admin_required
def gestion_usuarios(request):
    name = request.user.first_name
    return render(request, 'administrador/gestion_usuarios.html', {'nameadmin': name})

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
        is_normal = request.POST.get('normal', False)
        is_superuser = request.POST.get('superusuario', False)
        is_staff = request.POST.get('vendedor', False)

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
        user.is_normal = bool(is_normal)
        user.is_superuser = bool(is_superuser)
        user.is_staff = bool(is_staff) # Cambiar el is_vendedor
        user.save()

        messages.success(request, _("Usuario creado con exito"))
        return redirect('ver_usuarios_admin')
    
    return render(request, 'administrador/gestion_usuarios/crear_usuario.html')

# Vista Administrador Gestion Usuarios -ver usuario
@admin_required
def ver_usuarios_admin(request):
    # Llamo al procedimiento creado en mysql (el cuál está en la línea 801)
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


# Vista Administrador Gestion Usuarios modificar usuario
@admin_required
def modificar_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombres')
        apellido = request.POST.get('apellidos')
        username = request.POST.get('nombreusuario')
        email = request.POST.get('correo')
        is_normal = request.POST.get('normal')
        is_superuser = request.POST.get('superusuario', False)
        is_staff = request.POST.get('staff', False) # Esto es correcto

        if not (nombre and apellido and username and email):
            messages.error(request, _("Debes llenar todos los campos"))
            return redirect('modificar_usuario_admin', id_usuario=id_usuario)
        
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.username = username
        usuario.email = email
        usuario.is_normal = bool(is_normal)
        usuario.is_staff = bool(is_staff)  # Esto es correcto
        usuario.is_superuser = bool(is_superuser)
        usuario.save()

        success_message = _("Usuario modificado con éxito")
        return HttpResponseRedirect(reverse('ver_usuarios_admin') + f'?success_message={success_message}')
    
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

@login_required
def tipo_usuario_admin(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario) 
    if request.method == 'POST':
        # Obtener el rol existente del usuario
        rol_existente = usuario.rol
        
        # Obtener el nuevo rol del formulario
        nuevo_rol = request.POST.get('rol')
        
        # Verificar si se seleccionó un rol válido
        if nuevo_rol in ['cliente', 'vendedor']:
            # Actualizar el rol del usuario en la base de datos
            usuario.rol = nuevo_rol
            usuario.save()
            # Redirigir a la página de ver usuarios después de guardar los cambios
            return HttpResponseRedirect(reverse('ver_usuarios_admin'))
    
    # Si la solicitud no es POST o si no se pudo procesar correctamente, mostrar el formulario con el rol actual
    return render(request, 'administrador/gestion_usuarios/tipo_usuario_admin.html', {'usuario': usuario, 'rol_existente': usuario.rol})

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
            titulo_hab = request.session.get('titulo_hab')
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
            
            # Obtener tipo_metodo_pago
            row_tipo_metodo_pago = MetodoPago.objects.get(id_metodo_pago = 1)

            # Crear objeto Reserva
            reserva = Reserva(
                id_user = id_user,
                order_id = order_id,
                fecha_llegada = fecha_llegada_formateada,
                fecha_salida = fecha_salida_formateada,
                cant_adultos = cant_adultos,
                cant_ninos = cant_ninos,
                id_hab = row_hab,
                habitacion = titulo_hab,
                id_metodo_pago = row_tipo_metodo_pago,
                total = total,
                pago_inicial = pago_inicial,
                pago_pendiente = pago_pendiente,
            )
            # Guardar objeto Reserva
            reserva.save()
            # Obtener la reserva recién creada
            reserva_creada = Reserva.objects.latest('fecha_creacion')

            # Crear Reporte Reserva
            reporte_reserva = ReporteReserva(
                id_reserva = reserva_creada,
                dia_ingreso = fecha_llegada_formateada,
                dia_salida = fecha_salida_formateada
            )
            # Cambiar estado de habitación a "No Disponible"
            row_hab.estado = "No Disponible"
            row_hab.save()
            # Aqui sale el error -> Error: {"error":"get() returned more than one Reserva -- it returned 2!"}
            # Guardar Reporte Reserva en la base de datos
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
    return redirect('home')

# DROP PROCEDURE IF EXISTS obtener_todos_usuarios;
# DELIMITER $
# CREATE PROCEDURE obtener_todos_usuarios()
# BEGIN
# 	SELECT * FROM auth_user;
# END $
# DELIMITER ;
# CALL obtener_todos_usuarios();   
    

# VISTAS DEL VENDEDOR

# Vista Vendedor Home
@seller_required
def vendedor_home(request):
    name = request.user.first_name
    return render(request, 'vendedor/vendedor_home.html', {'nameseller': name})

# Vista Vendedor Gestion Reservas
@seller_required
def gestion_reservas_vendedor(request):
    name = request.user.first_name
    return render(request, 'vendedor/gestion_reservas_vendedor.html', {'nameseller': name})

# Vista Vendedor Gestion Reservas -crear
@seller_required
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
@seller_required
def eliminar_reserva_pacific_vendedor(request):
    reservas = Reserva.objects.all()
    if request.method == 'POST':
        # Obtener el input hidden id_reserva
        id_reserva = request.POST.get('id_reserva')
        # Obtener del input hidden el id_hab de la reserva
        id_hab = request.POST.get('id_hab')
        reserva = get_object_or_404(Reserva, id_reserva=id_reserva)
        reserva.delete()
        messages.success(request, _("Reserva Eliminada Exitosamente"))
        # Cuando se elimine una reserva, cambiar estado de habitación a "Disponible"
        habitacion = Habitacion.objects.get(pk= id_hab)
        # Cambiar estado a "Disponible"
        habitacion.estado = "Disponible"
        # Actualizar el estado en BBDD
        habitacion.save()
    
    return render(request, 'vendedor/gestion_reservas_vendedor/eliminar_reserva_pacific_vendedor.html',{'reservas': reservas})

# Vista Vendedor Gestion Reservas -modificar
@seller_required
def modificar_reserva_pacific_vendedor(request):
    if request.method == 'POST':
        id_reserva = request.POST.get('id_reserva')
        fecha_llegada = request.POST.get('fecha_llegada')
        fecha_salida = request.POST.get('fecha_salida')

        fecha_llegada_obj = datetime.strptime(fecha_llegada, '%Y-%m-%d').date()
        fecha_salida_obj = datetime.strptime(fecha_salida, '%Y-%m-%d').date()

        cant_adultos = request.POST.get('cant_adultos')
        cant_ninos = request.POST.get('cant_ninos')
        habitacion = request.POST.get('habitacion')
        tipo_metodo_pago = request.POST.get('tipo_metodo_pago')
        estado_pago = request.POST.get('estado_pago')
        
        # Obtener datos de reserva por id_reserva
        reserva = Reserva.objects.get(id_reserva = id_reserva)
        # Actualizar campos de reserva
        reserva.fecha_llegada = fecha_llegada_obj
        reserva.fecha_salida = fecha_salida_obj
        reserva.cant_adultos = cant_adultos
        reserva.cant_ninos = cant_ninos
        reserva.habitacion = habitacion
        reserva.estado_pago = estado_pago
        # Guardar actualizaciones de reserva
        reserva.save()

    reservas = Reserva.objects.all()

    for reserva in reservas:
        reserva.fecha_llegada = reserva.fecha_llegada.strftime('%Y-%m-%d')
        reserva.fecha_salida = reserva.fecha_salida.strftime('%Y-%m-%d')

    return render(request, 'vendedor/gestion_reservas_vendedor/modificar_reserva_pacific_vendedor.html', {'reservas':reservas})

# Vista Vendedor Gestion Reservas -ver calendario
@seller_required
def ver_calendario_pacific_vendedor(request):
    # Establecer la localización en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    # Obtener día actual
    dia_actual = datetime.now().day
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    # Obtener los días del mes actual
    nombre_mes_actual, dias_mes_actual = obtener_dias_mes(mes_actual, año_actual)
    nombre_mes_actual = nombre_mes_actual.capitalize()

    lista_dias = ['Lun.', 'Mar.', 'Mié.','Jue.','Vié.','Sáb.','Dom.']

    return render(request, 'vendedor/gestion_reservas_vendedor/ver_calendario_pacific_vendedor.html', {
        'dia_actual': dia_actual,
        'nombre_mes_actual': nombre_mes_actual,
        'dias_mes_actual': dias_mes_actual,
        'año_actual': año_actual,
        'lista_dias': lista_dias
    })

# Vista Vendedor Gestion Reservas -ver reserva
@seller_required
def ver_reserva_pacific_vendedor(request):
    reservas = Reserva.objects.all()
    return render(request, 'vendedor/gestion_reservas_vendedor/ver_reserva_pacific_vendedor.html',{'reservas':reservas})

@seller_required
def cerrarsesionvendedor(request):
    logout(request)
    return redirect('home')

# Serializadores API REST

class MetodoPagoListCreate(generics.ListCreateAPIView):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer

class ReservaListCreate(generics.ListCreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class ReporteReservaListCreate(generics.ListCreateAPIView):
    queryset = ReporteReserva.objects.all()
    serializer_class = ReporteReservaSerializer

class TipoHabitacionListCreate(generics.ListCreateAPIView):
    queryset = TipoHabitacion.objects.all()
    serializer_class = TipoHabitacionSerializer

class HabitacionListCreate(generics.ListCreateAPIView):
    queryset = Habitacion.objects.all()
    serializer_class = HabitacionSerializer

class DatosBancariosListCreate(generics.ListCreateAPIView):
    queryset = DatosBancarios.objects.all()
    serializer_class = DatosBancariosSerializer

# Enviar correo a cliente para realizar pago mediante paypal
# @admin_required
# def enviar_correo_paypal(request):
#     if request.method == 'POST' and request.is_ajax():
#         correo_electronico = request.POST.get('correo')

#         # Aquí puedes enviar el correo electrónico usando la función send_mail de Django
#         # Ejemplo:
#         send_mail(
#             'Asunto del correo',
#             'Cuerpo del correo',
#             'tu_correo@example.com',
#             [correo_electronico],
#             fail_silently=False,
#         )

#         return JsonResponse({'mensaje': 'Correo electrónico enviado con éxito.'})
#     else:
#         return JsonResponse({'error': 'La solicitud debe ser POST y AJAX.'}, status=400)
