from rest_framework import serializers
from .models import Cliente, Vehiculo, Servicio, Mecanico, DetalleServicio, OrdenReparacion

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields =  "__all__"
        read_only_fields = ('created_at')


class VehiculoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")

    class Meta:
        model = Vehiculo
        fields = "__all__"


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"


class  MecanicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecanico
        fields =  "__all__"

class DetalleServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleServicio
        fields = "__all__"

class OrdenReparacionSerializer(serializers.ModelSerializer):
    vehiculo_placa = serializers.ReadOnlyField(source="vehiculo.placa")
    mecanico_nombre = serializers.ReadOnlyField(source="mecanico.nombre")

    class Meta:
        model = OrdenReparacion
        fields = "__all__"


    




