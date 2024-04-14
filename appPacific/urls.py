from django.urls import path
from . import views
from .views import iniciosesion, cerrarsesion, misreservas, misdatos, administrador_home, crear_habitacion, crear_reserva_pacific, crear_usuario_admin, eliminar_habitacion, eliminar_reserva_pacific, eliminar_usuario_admin, gestion_habitaciones, gestion_reservas, gestion_usuarios, index, home, login, modificar_habitacion, modificar_reserva_pacific, modificar_reporte_reserva, modificar_usuario_admin, modificar_usuario_admin, registro, habitaciones, metodo_pago, transferencias, reserva_realizada, contacto, nosotros, tipo_usuario_admin, ver_calendario_pacific, ver_habitacion, ver_reserva_pacific, ver_usuarios_admin

urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name="home"),
    path('registro/', registro, name="registro"),
    path('iniciosesion/', iniciosesion, name='iniciosesion'),
    path('cerrarsesion/', cerrarsesion, name='cerrarsesion'),
    path('misreservas/', misreservas, name='misreservas'),
    path('misdatos/', misdatos, name='misdatos'),
    path('habitaciones/', habitaciones, name="habitaciones"),
    path('metodo_pago/', metodo_pago, name="metodo_pago"),
    path('transferencias/', transferencias, name="transferencias"),
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
    path('modificar_reporte_reserva/', modificar_reporte_reserva, name="modificar_reporte_reserva"),
    path('ver_calendario_pacific/', ver_calendario_pacific, name="ver_calendario_pacific"),
    path('ver_reserva_pacific/', ver_reserva_pacific, name="ver_reserva_pacific"),
    path('gestion_usuarios/', gestion_usuarios, name="gestion_usuarios"),
    path('gestion_usuarios/crear_usuario/', crear_usuario_admin, name='crear_usuario_admin'),
    path('gestion_usuarios/ver_usuario/', ver_usuarios_admin, name='ver_usuarios_admin'),
    path('gestion_usuarios/modificar_usuario/<int:id_usuario>/', modificar_usuario_admin, name='modificar_usuario_admin'),
    path('gestion_usuarios/eliminar_usuario/<int:id_usuario>/', eliminar_usuario_admin, name='eliminar_usuario_admin'),
    path('gestion_usuarios/tipo_usuario_admin/<int:id_usuario>/', tipo_usuario_admin, name='tipo_usuario_admin'),
    path('api/orders', views.create_order, name='create_order'),
    path('api/orders/<str:order_id>/capture', views.capture_order, name='capture_order'),
    path('cerrarsesionadmin/', views.cerrarsesionadmin, name='cerrarsesionadmin'),
]
