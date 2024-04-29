from rest_framework import serializers
from .models import MetodoPago, Reserva, ReporteReserva, TipoHabitacion, Habitacion, DatosBancarios

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id_metodo_pago', 'tipo_metodo_pago']

class TipoHabitacionSerializer(serializers.ModelSerializer):
    tipo_hab = serializers.CharField()

    class Meta:
        model = TipoHabitacion
        fields = ['id_tipo_hab', 'tipo_hab']

class HabitacionSerializer(serializers.ModelSerializer):
    id_tipo_hab = serializers.PrimaryKeyRelatedField(queryset=TipoHabitacion.objects.all())
    class Meta:
        model = Habitacion
        fields = ['id_hab', 'id_tipo_hab', 'titulo_hab', 'descripcion', 'titulo_en', 'descripcion_en', 'capacidad_max', 'precio', 'estado', 'imagen']

class DatosBancariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosBancarios
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    id_hab = HabitacionSerializer()
    id_metodo_pago = MetodoPagoSerializer()
    class Meta:
        model = Reserva
        fields = ['id_reserva', 'id_user', 'order_id', 'fecha_llegada', 'fecha_salida',
                  'cant_adultos', 'cant_ninos', 'id_hab', 'habitacion', 'id_metodo_pago',
                  'total', 'pago_inicial', 'pago_pendiente', 'estado_pago', 'fecha_creacion']

class ReporteReservaSerializer(serializers.ModelSerializer):
    id_reserva = ReservaSerializer()
    class Meta:
        model = ReporteReserva
        fields = ['id_reporte', 'id_reserva', 'dia_ingreso', 'hora_ingreso', 'dia_salida', 'hora_salida']


