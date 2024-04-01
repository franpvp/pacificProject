from django.urls import path

from .views import index, home, habitaciones, metodo_pago, reserva_realizada, contacto, nosotros

urlpatterns = [
    path('', index, name="index"),
    path('home/', home, name="home"),
    path('habitaciones/', habitaciones, name="habitaciones"),
    path('metodo_pago/', metodo_pago, name="metodo_pago"),
    path('contacto/', contacto, name="contacto"),
    path('reserva_realizada/', reserva_realizada, name="reserva_realizada"),
    path('nosotros/', nosotros, name="nosotros"),
]
