from django.test import TestCase
import pytest
from appPacific.models import MetodoPago, Reserva, ReporteReserva, TipoHabitacion, Habitacion, DatosBancarios
from appPacific.serializers import MetodoPagoSerializer, ReporteReservaSerializer, ReservaSerializer, ReporteReserva, TipoHabitacionSerializer, HabitacionSerializer, DatosBancariosSerializer
from datetime import datetime
from rest_framework.test import APITestCase

@pytest.mark.django_db
class MetodoPagoSerializerTest(TestCase):
    def setUp(self):
        self.metodo_pago_data = {
            'tipo_metodo_pago': 'Tarjeta de crédito'
        }

    def test_metodo_pago_serializer(self):
        serializer = MetodoPagoSerializer(data=self.metodo_pago_data)
        self.assertTrue(serializer.is_valid())
    

@pytest.mark.django_db
class TipoHabitacionSerializerTest(TestCase):
    def setUp(self):
        self.tipo_habitacion_data = {
            'id_tipo_hab': 1,
            'tipo_hab': 'Suite Presidencial'
        }
        self.tipo_habitacion = TipoHabitacion.objects.create(**self.tipo_habitacion_data)
        self.serializer = TipoHabitacionSerializer(instance=self.tipo_habitacion)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id_tipo_hab', 'tipo_hab']))

    def test_id_tipo_hab_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id_tipo_hab'], self.tipo_habitacion_data['id_tipo_hab'])

    def test_tipo_hab_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['tipo_hab'], self.tipo_habitacion_data['tipo_hab'])

@pytest.mark.django_db
class DatosBancariosSerializerTest(TestCase):
    def setUp(self):
        self.datos_bancarios_data = {
            'id_banco': 1,
            'beneficiario': 'John Doe',
            'cuenta': 'Cuenta de Ahorros',
            'nro_cuenta': '1234567890123456',
            'correo_banco': 'banco@example.com'
        }
        self.datos_bancarios = DatosBancarios.objects.create(**self.datos_bancarios_data)
        self.serializer = DatosBancariosSerializer(instance=self.datos_bancarios)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            set(['id_banco', 'beneficiario', 'cuenta', 'nro_cuenta', 'correo_banco'])
        )

    def test_id_banco_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['id_banco'], self.datos_bancarios_data['id_banco'])

    def test_beneficiario_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['beneficiario'], self.datos_bancarios_data['beneficiario'])

    def test_cuenta_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['cuenta'], self.datos_bancarios_data['cuenta'])

    def test_nro_cuenta_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['nro_cuenta'], self.datos_bancarios_data['nro_cuenta'])

    def test_correo_banco_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['correo_banco'], self.datos_bancarios_data['correo_banco'])

@pytest.mark.django_db   
class HabitacionSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear una instancia de TipoHabitacion para usarla en la prueba
        tipo_habitacion = TipoHabitacion.objects.create(
            tipo_hab='Suite'
        )
        # Crear una instancia de Habitacion para usarla en la prueba
        cls.habitacion = Habitacion.objects.create(
            id_hab=1,
            id_tipo_hab=tipo_habitacion,
            titulo_hab='Habitación Suite',
            descripcion='Una habitación cómoda con todas las comodidades necesarias.',
            titulo_en='Room Suite',
            descripcion_en='A comfortable room with all necessary amenities.',
            capacidad_max=4,
            precio='150000',
            estado='Disponible',
            imagen='datos_de_la_imagen_en_base64'
        )
        # Crear un serializador para la instancia de Habitacion
        cls.serializer = HabitacionSerializer(instance=cls.habitacion)


    def test_contains_expected_fields(self):
        expected_fields = {'id_hab', 'id_tipo_hab', 'titulo_hab', 'descripcion', 'titulo_en', 'descripcion_en', 'capacidad_max', 'precio', 'estado', 'imagen'}
        self.assertEqual(set(self.serializer.data.keys()), expected_fields)

    def test_id_hab_field_content(self):
        self.assertEqual(self.serializer.data['id_hab'], self.habitacion.id_hab)

    def test_id_tipo_hab_content(self):
        self.assertEqual(self.serializer.data['id_tipo_hab'], self.habitacion.id_tipo_hab.id_tipo_hab)

    def test_titulo_hab_content(self):
        self.assertEqual(self.serializer.data['titulo_hab'], 'Habitación Suite')

    def test_descripcion_content(self):
        self.assertEqual(self.serializer.data['descripcion'], 'Una habitación cómoda con todas las comodidades necesarias.')

    def test_titulo_en_content(self):
        self.assertEqual(self.serializer.data['titulo_en'], 'Room Suite')

@pytest.mark.django_db   
class ReservaSerializerTest(TestCase):
    def setUp(self):
        # Crear instancias de TipoHabitacion, Habitacion y MetodoPago para usar en la prueba
        tipo_habitacion = TipoHabitacion.objects.create(tipo_hab='Suite')
        self.habitacion = Habitacion.objects.create(
            id_hab=1,
            id_tipo_hab=tipo_habitacion,
            titulo_hab='Habitación Suite',
            descripcion='Una habitación espaciosa y lujosa.',
            titulo_en='Suite Room',
            descripcion_en='A spacious and luxurious room.',
            capacidad_max=2,
            precio=200,
            estado='Disponible',
            imagen='datos_de_la_imagen_en_base64'
        )

        metodo_pago = MetodoPago.objects.create(tipo_metodo_pago='Tarjeta de Crédito')

        # Crear una instancia de Reserva con los datos de prueba
        self.reserva_data = {
            'id_reserva': 1,
            'id_user': '1',
            'order_id': 'ABC123',
            'fecha_llegada': '2024-05-01',
            'fecha_salida': '2024-05-05',
            'cant_adultos': 2,
            'cant_ninos': 1,
            'id_hab': self.habitacion,  # Guarda solo el ID de la habitación
            'habitacion': self.habitacion.titulo_hab,
            'id_metodo_pago': metodo_pago,
            'total': 800,
            'pago_inicial': 200,
            'pago_pendiente': 600,
            'estado_pago': 'Pendiente',
        }

        self.reserva = Reserva.objects.create(**self.reserva_data)
        self.serializer = ReservaSerializer(instance=self.reserva)

    def test_contains_expected_fields(self):
        # Verifica si todos los campos esperados están presentes en el serializador
        data = self.serializer.data
        self.assertEqual(
            set(data.keys()),
            {'id_reserva', 'id_user', 'order_id', 'fecha_llegada', 'fecha_salida',
             'cant_adultos', 'cant_ninos', 'id_hab', 'habitacion', 'id_metodo_pago',
             'total', 'pago_inicial', 'pago_pendiente', 'estado_pago', 'fecha_creacion'}
        )

    def test_id_reserva_content(self):
        data = self.serializer.data
        self.assertEqual(data['id_reserva'], 1)

    def test_id_user_content(self):
        data = self.serializer.data
        self.assertEqual(data['id_user'], '1')

    def test_order_id(self):
        data = self.serializer.data
        self.assertEqual(data['order_id'], 'ABC123')

    def test_fecha_llegada(self):
        data = self.serializer.data
        self.assertEqual(data['fecha_llegada'], '2024-05-01')

    def test_fecha_salida(self):
        data = self.serializer.data
        self.assertEqual(data['fecha_salida'], '2024-05-05')

    def test_cant_adultos(self):
        data = self.serializer.data
        self.assertEqual(data['cant_adultos'], 2)

    def test_cant_ninos(self):
        data = self.serializer.data
        self.assertEqual(data['cant_ninos'], 1)

    def test_habitacion(self):
        data = self.serializer.data
        self.assertEqual(data['habitacion'], self.reserva_data['habitacion'])

    def test_total(self):
        data = self.serializer.data
        self.assertEqual(data['total'], 800)

    def test_pago_inicial(self):
        data = self.serializer.data
        self.assertEqual(data['pago_inicial'], 200)

    def test_pago_pendiente(self):
        data = self.serializer.data
        self.assertEqual(data['pago_pendiente'], 600)

    def test_estado_pago(self):
        data = self.serializer.data
        self.assertEqual(data['estado_pago'], 'Pendiente')


@pytest.mark.django_db
class TestReporteReservaSerializer(TestCase):
    def setUp(self):
         self.metodo_pago = MetodoPago.objects.create(tipo_metodo_pago='Suite')
         self.tipo_habitacion = TipoHabitacion.objects.create(tipo_hab='Tarjeta de credito')
         self.habitacion = Habitacion.objects.create(
            id_hab=1,
            id_tipo_hab=self.tipo_habitacion,
            titulo_hab='Habitación Suite',
            descripcion='Una habitación espaciosa y lujosa.',
            titulo_en='Suite Room',
            descripcion_en='A spacious and luxurious room.',
            capacidad_max=2,
            precio=200,
            estado='Disponible',
            imagen='datos_de_la_imagen_en_base64'
         )
         self.reserva = Reserva.objects.create(
            id_reserva=1,
            id_user='1',
            order_id='ABC123',
            fecha_llegada='2024-05-01',
            fecha_salida='2024-05-05',
            cant_adultos=2,
            cant_ninos=1,
            id_hab=self.habitacion, 
            habitacion='Suite',
            id_metodo_pago = self.metodo_pago,
            total=800,
            pago_inicial=200,
            pago_pendiente=600,
            estado_pago='Pendiente',
        )
         self.reporte_reserva_data = {
            'id_reporte': 1,
            'id_reserva': self.reserva,
            'dia_ingreso': '2024-05-01',
            'hora_ingreso': '09:00:00',
            'dia_salida': '2024-05-05',
            'hora_salida': '12:00:00'
        }
         self.reporte_reserva = ReporteReserva.objects.create(**self.reporte_reserva_data)
         self.serializer = ReporteReservaSerializer(instance=self.reporte_reserva)
    def test_contains_expected_fields(self):
        data = self.serializer.data
        assert set(data.keys()) == {'id_reporte', 'id_reserva', 'dia_ingreso', 'hora_ingreso', 'dia_salida', 'hora_salida'}

    def test_id_reporte_content(self):
        data = self.serializer.data
        assert data['id_reporte'] == self.reporte_reserva.id_reporte
    
    def test_dia_ingreso_content(self):
        data = self.serializer.data
        assert data['dia_ingreso'] == self.reporte_reserva.dia_ingreso

    def test_hora_ingreso_content(self):
        data = self.serializer.data
        assert data['hora_ingreso'] == self.reporte_reserva.hora_ingreso
    
    def test_dia_salida_content(self):
        data = self.serializer.data
        assert data['dia_salida'] == self.reporte_reserva.dia_salida
    
    def test_hora_salida_content(self):
        data = self.serializer.data
        assert data['hora_salida'] == self.reporte_reserva.hora_salida


