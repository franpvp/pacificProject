from django.shortcuts import render
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import RegistroUsuario,TipoUsuario
import requests

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

# Vista Registro
def registro(request):
    return render(request, 'registration/registro.html')

# Vista Contacto
def contacto(request):
    return render(request, 'app/contacto.html')


# Vista Habitaciones
def habitaciones(request):
    return render(request, 'app/habitaciones.html')

# Vista Método Pago
def metodo_pago(request):
    return render(request, 'app/metodo_pago.html')

# Vista Reserva Realizada
def reserva_realizada(request):
    return render(request, 'app/reserva_realizada.html')