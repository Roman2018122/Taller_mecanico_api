from rest_framework import serializers
from datetime import date

from .models import Cliente, Vehiculo, Servicio, Mecanico, DetalleServicio, OrdenReparacion



# Convierte y valida datos del modelo Cliente para la API
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields =  "__all__"
        read_only_fields = ('created_at',)
        
    def validate_nombre(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )

        return value
        

    def validate_telefono(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "El teléfono solo puede contener números."
            )

        return value

# Convierte datos del modelo Vehiculo y agrega información del cliente
class VehiculoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")

    class Meta:
        model = Vehiculo
        fields = "__all__"

    def validate_anio(self, value):
        anio_actual = date.today().year

        if value < 1950:
            raise serializers.ValidationError(
                "El año del vehículo no es válido."
            )

        if value > anio_actual + 1:
            raise serializers.ValidationError(
                "El año del vehículo no es válido."
            )

        return value

# Maneja la serialización y validación del modelo Servicio
class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = "__all__"

    def validate_nombre(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre del servicio debe contener mas de 3 caracteres"
            )

        return value

    def validate_precio_referencial(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor que cero."
            )

        return value


# Serializa datos del modelo Mecanico y valida teléfono

class  MecanicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecanico
        fields =  "__all__"

    def validate_telefono(self, value):

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError(
                "El teléfono solo puede contener números."
            )

        return value
    


# Serializa órdenes de reparación y muestra datos relacionados del vehículo y mecánico
class OrdenReparacionSerializer(serializers.ModelSerializer):
    vehiculo_placa = serializers.ReadOnlyField(source="vehiculo.placa")
    mecanico_nombre = serializers.ReadOnlyField(source="mecanico.nombre")

    class Meta:
        model = OrdenReparacion
        fields = "__all__"

    def validate(self, data):

        fecha_ingreso = data.get("fecha_ingreso")
        fecha_salida = data.get("fecha_salida")

        if (
            fecha_ingreso
            and fecha_salida
            and fecha_salida < fecha_ingreso
        ):
            raise serializers.ValidationError(
                "La fecha de salida no puede ser menor que la fecha de ingreso."
            )

        return data


# Serializa detalle de servicios y valida cantidad y precio
class DetalleServicioSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetalleServicio
        fields = "__all__"
        read_only_fields = ("subtotal",)

    def validate_precio_unitario(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "El precio unitario debe ser mayor que cero."
            )

        return value

    def validate_cantidad(self, value):

        if value < 1:
            raise serializers.ValidationError(
                "La cantidad debe ser al menos 1."
            )

        return value



