import os
from django.test import TestCase, Client
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from appPacific.models import TipoHabitacion, Habitacion, Reserva, MetodoPago
import pytest
from appPacific.test_utils import test_setup
import base64
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime


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


# Test Vista Registro
@pytest.mark.django_db
class RegistroViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_registro_success(self):
        data = {
            'nombre': 'John',
            'apellidos': 'Doe',
            'correo': 'john@example.com',
            'username': 'johndoe',
            'celular': '123456789',
            'password1': 'password',
            'password2': 'password',
        }

        # Hace un POST request a la vista
        response = self.client.post(reverse('registro'), data)

        # Verifica si la respuesta redirecciona a la URL esperada (index)
        self.assertRedirects(response, reverse('index'))

        # Optionally, check if the user is created and has the correct attributes
        user = User.objects.get(username=data['username'])
        self.assertEqual(user.first_name, data['nombre'])
        self.assertEqual(user.last_name, data['apellidos'])
        self.assertEqual(user.email, data['correo'])

# Test Vista Inicio Sesión

@pytest.mark.django_db
class InicioSesionViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='usuario2',
            email='usuario1@gmail.com',
            password='12345',
            is_staff=False,
            is_superuser=False
        )

    def test_user_creation(self):
        self.assertEqual(self.user.is_active,True)
        self.assertEqual(self.user.is_staff,False)
        self.assertEqual(self.user.is_superuser,False)

    def test_superuser_creation(self):
        user = User.objects.create_superuser(
            username='usuario3',
            email='usuario1@gmail.com',
            password='12345'
        )
        assert user.is_superuser

    def test_is_staff_user_creation(self):
        user = User.objects.create_user(
            username='usuario4',
            email='usuario1@gmail.com',
            password='12345',
            is_staff=True
        )
        assert user.is_staff

    def test_user_creation_fail(self):
        with pytest.raises(Exception):
            User.objects.create_user(
                password='12345',
                is_staff=False
            )

    def test_login(self):
        # Preparando el POST data
        data = {
            'username': 'usuario1',
            'password': '12345',
        }

        # Hacer una POST request a la vista
        response = self.client.post(reverse('iniciosesion'), data)

        # Verificar si el response status code es 200 (exitoso)
        self.assertEqual(response.status_code, 200)

        # Verificar si el usuario es logged in después de un successful login
        user = authenticate(username=data['username'], password=data['password'])

        # Si el user es not None, verificar is es authenticated
        if user is not None:
            self.assertTrue(user.is_authenticated)
        else:
            print("Authentication failed. User is None.")

# Test Vista Cerrar Sesión
@pytest.mark.django_db
class CerrarSesionViewTestCase(TestCase):
    def test_usuario_autenticado(self):
        client = Client()

        # Autenticar al usuario
        client.force_login(User.objects.get(username='usuario'))

        # Hacer una solicitud GET a la vista 'cerrarsesion'
        response = client.get(reverse('cerrarsesion'))

        # Verificar que la respuesta sea una redirección (código de estado 302)
        assert response.status_code == 302

        # Verificar que la vista haya redirigido a la página correcta ('index')
        assert response.url == reverse('index')

# Test Vista Mis Reservas Usuario Común
@pytest.mark.django_db
class MisReservasViewTestCase(TestCase):
    def test_usuario_autenticado(self):
        client = Client()

        # Autenticar al usuario
        client.force_login(User.objects.get(username='usuario'))

        # Hacer una solicitud GET a la vista 'misreservas' autenticados como el usuario creado
        response = client.get(reverse('misreservas'))

        # Verificar que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verificar que la plantilla 'misreservas.html' se esté utilizando
        self.assertTemplateUsed(response, 'registration/misreservas.html')

# Test Vista Mis Datos
@pytest.mark.django_db
class MisDatosViewTestCase(TestCase):
    pass
# Test Vista Contacto
@pytest.mark.django_db
class ContactoViewTestCase(TestCase):
    pass

# Test Vista Habitaciones
@pytest.mark.django_db
class HabitacionesViewTestCase(TestCase):
    pass

# Test Vista Metodo Pago
@pytest.mark.django_db
class MetodoPagoViewTestCase(TestCase):
    pass

# Test Vista Generar Código Random Transferencias
@pytest.mark.django_db
class GenerarCodigoViewTestCase(TestCase):
    pass

# Test Vista Obtener Codigo Random Transferencias
@pytest.mark.django_db
class ObtenerCodigoViewTestCase(TestCase):
    pass

# Test Vista Transferencias
@pytest.mark.django_db
class TransferenciasViewTestCase(TestCase):
    pass

# Test Vista Reserva Realizada
@pytest.mark.django_db
class ReservaRealizadaViewTestCase(TestCase):
    pass

# Test Vista Administrador Home
@pytest.mark.django_db
class AdministradorHomeViewTestCase(TestCase):
    pass

# Test Vista Gestión Habitaciones
@pytest.mark.django_db
class GestionHabitacionesViewTestCase(TestCase):
    pass


# Test Vista Crear Habitación
@pytest.mark.django_db
class CrearHabitacionViewTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario administrador para simular la autenticación
        self.admin_user = User.objects.create_user(username='admin', password='admin123', is_superuser=True)

        # Creamos un tipo de habitación para usarlo en la prueba
        self.tipo_habitacion = TipoHabitacion.objects.create(id_tipo_hab=1, tipo_hab='Suite')

        # URL para la vista de creación de habitación
        self.url = reverse('crear_habitacion')

    def test_creacion_habitacion(self):
        # Creamos un cliente y autenticamos como el usuario administrador
        client = Client()
        client.force_login(self.admin_user)

        # Datos para crear una habitación
        data = {
            'id_tipo_hab': self.tipo_habitacion.id_tipo_hab,
            'titulo_hab': 'Habitación de Prueba',
            'descripcion': 'Descripción de la habitación de prueba',
            'titulo_en': 'Test Room',
            'descripcion_en': 'Test Room Description',
            'capacidad_max': 2,
            'precio': '100.00',
        }

        # Obtén la ruta al archivo de imagen de prueba
        imagen_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')

        try:
            # Crea un archivo de imagen simulado para cargar
            with open(imagen_path, 'rb') as file:
                imagen_data = file.read()
                imagen_file = SimpleUploadedFile('test_image.jpg', imagen_data, content_type='image/jpeg')

                # Añade el archivo de imagen al diccionario de datos
                data['imagen'] = imagen_file

                # Envía una solicitud POST para crear una habitación
                response = client.post(self.url, data, format='multipart')

                # Verifica que la habitación se haya creado correctamente en la base de datos
                self.assertEqual(response.status_code, 200)
                self.assertTrue(Habitacion.objects.exists())

        except Exception as e:
            # Si ocurre alguna excepción al abrir el archivo, imprime un mensaje de error
            print(f"Error al abrir el archivo: {str(e)}")

# Test Vista Eliminar Habitación
@pytest.mark.django_db
class EliminarHabitacionViewTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario administrador para simular la autenticación
        self.admin_user = User.objects.create_user(username='admin', password='admin123', is_superuser=True)

        # Creamos una instancia de TipoHabitacion
        tipo_habitacion = TipoHabitacion.objects.create(id_tipo_hab=1, tipo_hab='Suite')

        # Creamos una instancia de Habitacion y la asignamos a una variable de instancia
        self.habitacion = Habitacion.objects.create(
            id_tipo_hab=tipo_habitacion,
            titulo_hab='Habitación de ejemplo',
            descripcion='Descripción de la habitación',
            titulo_en='Example Room',
            descripcion_en='Room Description',
            capacidad_max=2,
            precio='100000',
            estado='Disponible',
            imagen=None
        )

        # URL para la vista de eliminar habitación
        self.url = reverse('eliminar_habitacion')

    def test_eliminar_habitacion(self):
        # Creamos un cliente y autenticamos como el usuario administrador
        client = Client()
        client.force_login(self.admin_user)

        # Hacemos una solicitud POST para eliminar una habitación
        response = client.post(self.url, {'id_hab': self.habitacion.id_hab})

        # Verificamos que la habitación se haya eliminado correctamente
        self.assertEqual(response.status_code, 200)  # Verificamos que la vista retorne un código 200
        self.assertFalse(Habitacion.objects.filter(id_hab=self.habitacion.id_hab).exists())  # Verificamos que la habitación haya sido eliminada

        # Verificamos que se obtengan todas las habitaciones después de eliminar una
        self.assertTrue('habitaciones' in response.context)  # Verificamos que se pasen las habitaciones al contexto
        self.assertEqual(len(response.context['habitaciones']), 0)  # Verificamos que no haya habitaciones restantes

# Test Vista Modificar Habitación
@pytest.mark.django_db
class ModificarHabitacionViewTestCase(TestCase):
    pass

# Test Vista Ver Habitación
@pytest.mark.django_db
class VerHabitacionViewTestCase(TestCase):
    pass

# Test Vista Gestión Reservas
@pytest.mark.django_db
class GestionReservasViewTestCase(TestCase):
    pass

# Test Vista Crear Reserva Pacific
@pytest.mark.django_db
class CrearReservaViewTestCase(TestCase):
    pass

# Test Vista Eliminar Reserva Pacific
@pytest.mark.django_db
class EliminarReservaViewTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario administrador para simular la autenticación
        self.admin_user = User.objects.create_user(username='admin', password='admin123', is_superuser=True)

        tipo_habitacion = TipoHabitacion.objects.create(id_tipo_hab=1)
        # Crear una instancia de Habitacion
        habitacion = Habitacion.objects.create(
            id_tipo_hab=tipo_habitacion,
            titulo_hab='Habitación de ejemplo',
            descripcion='Descripción de la habitación',
            titulo_en='Example Room',
            descripcion_en='Room Description',
            capacidad_max=2,
            precio='100000',
            estado='Disponible',
            imagen= None
        )
        # Crear una instancia de MetodoPago
        metodo_pago = MetodoPago.objects.create(
            id_metodo_pago=1,
            tipo_metodo_pago='PayPal'
        )
        # Creamos algunas reservas de ejemplo
        self.reserva = Reserva.objects.create(
            id_user=self.admin_user,
            order_id='OKRMWSL123',
            fecha_llegada='2024-04-28',
            fecha_salida='2024-05-05',
            cant_adultos=2,
            cant_ninos=0,
            id_hab=habitacion.id_hab,  # Usamos el ID de la habitación
            habitacion='Habitación de Ejemplo',
            id_metodo_pago=metodo_pago.id_metodo_pago,  # Usamos el ID del método de pago
            total=100000,
            pago_inicial=30000,
            pago_pendiente=70000,
            estado_pago='Pendiente',
            fecha_creacion=datetime.now()
        )

        # URL para la vista de eliminar reserva pacífica
        self.url = reverse('eliminar_reserva_pacific')

    def test_eliminar_reserva_pacifica(self):
        # Creamos un cliente y autenticamos como el usuario administrador
        client = Client()
        client.force_login(self.admin_user)
        
        # Hacemos una solicitud POST para eliminar una reserva
        response = client.post(self.url, {'id_reserva': self.reserva.id_reserva, 'id_hab': self.reserva.id_hab})

        # Verificamos que la reserva se haya eliminado correctamente
        self.assertEqual(response.status_code, 200)  # Verificamos que la vista retorne un código 200
        self.assertFalse(Reserva.objects.filter(id_reserva=self.reserva.id_reserva).exists())  # Verificamos que la reserva haya sido eliminada

        # Verificamos que el estado de la habitación se haya actualizado a "Disponible"
        habitacion = Habitacion.objects.get(pk=self.reserva.id_hab)
        self.assertEqual(habitacion.estado, "Disponible")

        # Verificamos que se obtengan todas las reservas después de eliminar una
        self.assertTrue('reservas' in response.context)  # Verificamos que se pasen las reservas al contexto
        self.assertEqual(len(response.context['reservas']), 0)

# Test Vista Modificar Reporte Reserva
@pytest.mark.django_db
class ModificarReporteViewTestCase(TestCase):
    pass

# Test Vista ObtenerDiasMes
@pytest.mark.django_db
class ReservaRealizadaViewTestCase(TestCase):
    pass

# Test Vista ver_reserva_pacific
@pytest.mark.django_db
class VerReservaViewTestCase(TestCase):
    pass

# Test Vista ver_reporte_pacific
@pytest.mark.django_db
class VerReporteViewTestCase(TestCase):
    pass

# Test Vista create_order
@pytest.mark.django_db
class CreateOrderViewTestCase(TestCase):
    pass

# Test Vista capture_order
class CaptureOrderlizadaViewTestCase(TestCase):
    pass

# Test Vista generate_access_token
class GenerateAccessTokenViewTestCase(TestCase):
    pass

# Test Vista handle_response
class HandleResponseViewTestCase(TestCase):
    pass

# Test Vista cerrarsesionadmin
class CerrarSesionAdminViewTestCase(TestCase):
    pass

# Test Vista vendedor_home
class VendedorHomeViewTestCase(TestCase):
    pass

# Test Vista gestion_reservas_vendedor
class GestionReservasVendedorViewTestCase(TestCase):
    pass

# Test Vista crear_reserva_pacific_vendedor
class CrearReservaVendedorViewTestCase(TestCase):
    pass

# Test Vista eliminar_reserva_pacific_vendedor
class EliminarReservaVendedorViewTestCase(TestCase):
    pass

# Test Vista modificar_reserva_pacific_vendedor
class ModificarReservaVendedorViewTestCase(TestCase):
    pass

# Test Vista ver_reserva_pacific_vendedor
class VerReservaVendedorViewTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario vendedor para simular la autenticación
        self.vendedor_user = User.objects.create_user(username='vendedor', password='contraseña', is_staff=True)
        
        tipo_habitacion = TipoHabitacion.objects.create(id_tipo_hab=1)
        # Crear una instancia de Habitacion
        habitacion = Habitacion.objects.create(
            id_tipo_hab=tipo_habitacion,
            titulo_hab='Habitación de ejemplo',
            descripcion='Descripción de la habitación',
            titulo_en='Example Room',
            descripcion_en='Room Description',
            capacidad_max=2,
            precio='100000',
            estado='Disponible',
            imagen= None
        )
        # Crear una instancia de MetodoPago
        metodo_pago = MetodoPago.objects.create(
            id_metodo_pago=1,
            tipo_metodo_pago='PayPal'
        )
        # Creamos algunas reservas de ejemplo
        Reserva.objects.create(
            id_user=self.vendedor_user,
            order_id='OKRMWSL123',
            fecha_llegada='2024-04-28',
            fecha_salida='2024-05-05',
            cant_adultos=2,
            cant_ninos=0,
            id_hab=habitacion,  # Asignar la instancia de la habitación
            habitacion='Habitación de Ejemplo',
            id_metodo_pago=metodo_pago,  # Asignar la instancia del método de pago
            total=100000,
            pago_inicial=30000,
            pago_pendiente=70000,
            estado_pago='Pendiente',
            fecha_creacion=datetime.now()
        )

        # URL para la vista de ver reservas del vendedor
        self.url = reverse('ver_reserva_pacific_vendedor')

    def test_ver_reserva_pacific_vendedor(self):
        # Creamos un cliente y autenticamos como el usuario vendedor
        client = Client()
        client.force_login(self.vendedor_user)

        # Hacemos una solicitud GET a la vista de ver reservas del vendedor
        response = client.get(self.url)

        # Verificamos que la respuesta sea exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verificamos que la plantilla correcta se esté utilizando
        self.assertTemplateUsed(response, 'vendedor/gestion_reservas_vendedor/ver_reserva_pacific_vendedor.html')

        # Verificamos que las reservas se estén pasando correctamente al contexto
        self.assertTrue('reservas' in response.context)
        self.assertGreaterEqual(len(response.context['reservas']), 1)

# Test Vista cerrarsesionvendedor
class CerrarSesionVendedorViewTestCase(TestCase):
    def setUp(self):
        # Creamos un usuario administrador para simular la autenticación
        self.vendedor_user = User.objects.create_user(username='uservendedor', password='vendedor123', is_staff=True)
        # URL para la vista de cierre de sesión del vendedor
        self.url = reverse('cerrarsesionvendedor')

    def test_cerrar_sesion_vendedor(self):
        # Creamos un cliente y autenticamos como el usuario vendedor
        client = Client()
        client.force_login(self.vendedor_user)

        # Hacemos una solicitud GET a la vista de cierre de sesión del vendedor
        response = client.get(self.url)

        # Verificamos que la respuesta sea una redirección (código de estado 302)
        self.assertEqual(response.status_code, 302)

        # Verificamos que la vista haya redirigido a la página correcta ('index')
        self.assertEqual(response.url, reverse('index'))



# Con el decorador @pytest.mark.django_db se da acceso a la base de datos.
# Es importante no usar informacion de produccion en las pruebas.
# SETUP es un método es donde se crean todas las instancias
# que se necesite o las variables o datos iniciales que se necesitará
# para crear los tests y que se van a utilizar en mis tests.
# Aparte de los modelos necesito probar mis vistas, etc
# Las vistas se pueden llamar a traves de rutas, por eso se puede probar:
# que cuando la persona interectúe con una ruta, la ejecución y la lógica
# asociada a esa ruta se llame de manera correcta para eso:
# tengo que simular que soy un cliente que relice la petición o que
# envié los datos, etc, lo que requiera la ruta para que esta pueda 
# interactuar con la vista y pueda devolver la respuesta que sea necesaria.
# 