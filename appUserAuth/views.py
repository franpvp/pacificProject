from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

# Vista Registro

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

# Vista Login

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
                return render(request,'app/home.html',{'name':name})
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
    return redirect('home')

# Vistas Relacionadas con el usuario registrado:

@login_required
def misreservas(request):
    return render(request, 'registration/mireserva.html')

@login_required
def misdatos(request):
    return render(request, 'registration/datopersonal.html')
