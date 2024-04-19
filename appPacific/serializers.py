from rest_framework import serializers
from .models import MetodoPago, Reserva, ReporteReserva, TipoHabitacion, Habitacion, DatosBancarios

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class ReporteReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteReserva
        fields = '__all__'

class TipoHabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHabitacion
        fields = '__all__'

class HabitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitacion
        fields = '__all__'

class DatosBancariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosBancarios
        fields = '__all__'
