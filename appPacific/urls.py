from django.urls import path
from . import views
from .views import ReservaListCreateAPIView, crear_reserva_pacific_vendedor, eliminar_reserva_pacific_vendedor, gestion_reservas_vendedor, iniciosesion, cerrarsesion, misreservas, misdatos, administrador_home, crear_habitacion, crear_reserva_pacific, crear_usuario_admin, eliminar_habitacion, eliminar_reserva_pacific, eliminar_usuario_admin, gestion_habitaciones, gestion_reservas, gestion_usuarios, index, home, login, modificar_habitacion, modificar_reserva_pacific, modificar_reporte_reserva, modificar_reserva_pacific_vendedor, modificar_usuario_admin, modificar_usuario_admin, registro, habitaciones, metodo_pago, transferencias, reserva_realizada, contacto, nosotros, tipo_usuario_admin, vendedor_home, ver_calendario_pacific, ver_calendario_pacific_vendedor, ver_habitacion, ver_reserva_pacific, ver_reporte_pacific, ver_reserva_pacific_vendedor, ver_usuarios_admin
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from .views import (MetodoPagoListCreate, ReporteReservaListCreate, TipoHabitacionListCreate, 
                    HabitacionListView, DatosBancariosListCreate)

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
    path('ver_reporte_pacific/', ver_reporte_pacific, name="ver_reporte_pacific"),
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
    path('vendedor_home/', vendedor_home, name="vendedor_home"),
    path('gestion_reservas_vendedor/', gestion_reservas_vendedor, name="gestion_reservas_vendedor"),
    path('crear_reserva_pacific_vendedor/', crear_reserva_pacific_vendedor, name="crear_reserva_pacific_vendedor"),
    path('eliminar_reserva_pacific_vendedor/', eliminar_reserva_pacific_vendedor, name="eliminar_reserva_pacific_vendedor"),
    path('modificar_reserva_pacific_vendedor/', modificar_reserva_pacific_vendedor, name="modificar_reserva_pacific_vendedor"),
    path('ver_calendario_pacific_vendedor/', ver_calendario_pacific_vendedor, name="ver_calendario_pacific_vendedor"),
    path('ver_reserva_pacific_vendedor/', ver_reserva_pacific_vendedor, name="ver_reserva_pacific_vendedor"),
    path('cerrarsesionvendedor/', views.cerrarsesionvendedor, name='cerrarsesionvendedor'),
    path('cerrarsesionadmin/', views.cerrarsesionadmin, name='cerrarsesionadmin'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="recuperacion/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="recuperacion/reset_password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="recuperacion/reset_password_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="recuperacion/reset_password_complete.html"), name="password_reset_complete"),
    path('metodo_pago/', MetodoPagoListCreate.as_view(), name='metodo-pago-list-create'),
    path('reserva/', ReservaListCreateAPIView.as_view(), name='reserva-list-create'),
    path('reporte_reserva/', ReporteReservaListCreate.as_view(), name='reporte-reserva-list-create'),
    path('tipo_habitacion/', TipoHabitacionListCreate.as_view(), name='tipo-habitacion-list-create'),
    path('habitacion/', HabitacionListView.as_view(), name='habitacion-list-create'),
    path('datos_bancarios/', DatosBancariosListCreate.as_view(), name='datos-bancarios-list-create'),
]