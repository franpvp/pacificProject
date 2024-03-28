from django.urls import path

from .views import administrador_home, crear_habitacion, crear_reserva_pacific, crear_usuario, eliminar_habitacion, eliminar_reserva_pacific, eliminar_usuario, gestion_habitaciones, gestion_reservas, gestion_usuarios, index, home, login, modificar_habitacion, modificar_reserva_pacific, modificar_usuario, registro, habitaciones, metodo_pago, reserva_realizada, contacto, nosotros, ver_calendario_pacific, ver_habitacion, ver_reserva_pacific, ver_usuario

urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name="home"),
    path('login/', login, name="login"),
    path('registro/', registro, name="registro"),
    path('habitaciones/', habitaciones, name="habitaciones"),
    path('metodo_pago/', metodo_pago, name="metodo_pago"),
    path('contacto/', contacto, name="contacto"),
    path('reserva_realizada/', reserva_realizada, name="reserva_realizada"),
    path('nosotros/', nosotros, name="nosotros"),
    path('administrador_home/', administrador_home, name="administrador_home"),
    path('gestion_habitaciones/', gestion_habitaciones, name="gestion_habitaciones"),
    path('crear_habitacion/', crear_habitacion, name="crear_habitacion"),
    path('eliminar_habitacion/', eliminar_habitacion, name="eliminar_habitacion"),
    path('modificar_habitacion/', modificar_habitacion, name="modificar_habitacion"),
    path('ver_habitacion/', ver_habitacion, name="ver_habitacion"),
    path('gestion_reservas/', gestion_reservas, name="gestion_reservas"),
    path('crear_reserva_pacific/', crear_reserva_pacific, name="crear_reserva_pacific"),
    path('eliminar_reserva_pacific/', eliminar_reserva_pacific, name="eliminar_reserva_pacific"),
    path('modificar_reserva_pacific/', modificar_reserva_pacific, name="modificar_reserva_pacific"),
    path('ver_calendario_pacific/', ver_calendario_pacific, name="ver_calendario_pacific"),
    path('ver_reserva_pacific/', ver_reserva_pacific, name="ver_reserva_pacific"),
    path('gestion_usuarios/', gestion_usuarios, name="gestion_usuarios"),
    path('crear_usuario/', crear_usuario, name="crear_usuario"),
    path('eliminar_usuario/', eliminar_usuario, name="eliminar_usuario"),
    path('modificar_usuario/', modificar_usuario, name="modificar_usuario"),
    path('ver_usuario/', ver_usuario, name="ver_usuario"),
]
