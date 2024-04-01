from django.urls import path
from .import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
    path('cerrarsesion/', views.cerrarsesion, name='cerrarsesion'),
    path('misreservas/', views.misreservas, name='misreservas'),
    path('misdatos/', views.misdatos, name='misdatos'),
]
