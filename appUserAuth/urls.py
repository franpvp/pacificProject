from django.urls import path
from .import views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('iniciosesion/', views.iniciosesion, name='iniciosesion'),
]
