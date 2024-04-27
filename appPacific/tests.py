from django.test import TestCase
import pytest
from django.urls import reverse

class IndexViewTestCase(TestCase):
    def test_redireccion_despues_envio_formulario(self):
        # Simulamos una solicitud POST con datos válidos
        data = {
            'fecha_llegada': '2024-04-26',
            'fecha_salida': '2024-04-30',
            'cant_adultos': '1',
            'cant_ninos': '0'
        }

        # Hacemos la solicitud POST a la vista 'index'
        response = self.client.post(reverse('index'), data)

        # Verificamos que se redirige correctamente después del envío del formulario
        self.assertRedirects(response, reverse('habitaciones'))

    def test_validacion_campos_vacios(self):
        # Simulamos una solicitud POST con campos de fechas y número de adultos vacíos
        data = {
            'fecha_llegada': '',
            'fecha_salida': '',
            'cant_adultos': '0',
            'cant_ninos': '0'
        }

        # Hacemos la solicitud POST a la vista 'index'
        response = self.client.post(reverse('index'), data)

        # Verificamos que se muestra un mensaje de error
        self.assertContains(response, "Por favor, completa las fechas de llegada y salida")

