from django.test import TestCase, Client
from django.urls import reverse
import pytest

# Test Vista Index
@pytest.mark.django_db
class IndexViewTestCase(TestCase):
    def test_form_post(self):
        client = Client()

        # Creamos una solicitud POST con datos válidos
        data = {
            'fecha_llegada_formateada': '2024-04-26',
            'fecha_salida_formateada': '2024-04-30',
            'contador_adultos': '2',
            'contador_ninos': '0'
        }

        # Enviamos la solicitud POST al endpoint de 'habitaciones' utilizando el cliente
        response = client.post(reverse('habitaciones'), data)
        
        # Verificamos que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Verificamos que la vista haya redirigido a la página correcta
        self.assertEqual(response.url, reverse('index'))

        # Ahora probamos la vista 'index' directamente
        response_index = self.client.get(reverse('index'))
        
        # Verificamos que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response_index.status_code, 200)


# Test Vista Index
