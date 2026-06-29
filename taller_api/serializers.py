from rest_framework import serializers
from datetime import date, timezone

from .models import (
    Marca,
    Proveedor,
    ModeloVehiculo,
    Especialidades,
    RolSistema,
    PerfilUsuario,
    Cliente,
    Vehiculo,
    Servicio,
    Mecanico,
    CitaWeb,
    OrdenReparacion,
    DetalleServicio,
    Repuesto,
    CompraInventario,
    DetalleCompraInventario,
    DetalleRepuestoOrden,
    Factura,
    RegistroPago,
    MetodoPago

    
)
##=====================================================
## TABLAS BASE INDEPENDIENTES (Sin dependencias)
## ========================================================

##CLIENTE SERIALIZER
## Convierte y valida datos del modelo Cliente para la API
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

#Marca de vehiculos
# Maneja la conversión y validación del modelo Marca de vehículos/repuestos
class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = "__all__"

    def validate_nombre(self, value):
        # Limpia espacios en blanco extras al inicio y al final
        value = value.strip()

        # Validación de longitud mínima
        if len(value) < 2:
            raise serializers.ValidationError(
                "El nombre de la marca debe tener al menos 2 caracteres."
            )

        return value
## PROVEEDORES DE REPUESTOS 
# Maneja la conversión y validación del modelo Proveedor para el control de inventario
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"

    def validate_nombre_empresa(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre de la empresa debe tener al menos 3 caracteres."
            )
        return value

    def validate_ruc_nit(self, value):
        value = value.strip()
        # Validación para evitar caracteres extraños en la identificación fiscal
        if len(value) < 5:
            raise serializers.ValidationError(
                "El RUC/NIT proporcionado es demasiado corto."
            )
        return value

    def validate_telefono(self, value):
        value = value.strip()
        # Remueve caracteres comunes de formato si el usuario envía por ejemplo "(02) 234-567"
        # para validar si en el fondo son solo números
        clean_phone = value.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
        
        if not clean_phone.isdigit():
            raise serializers.ValidationError(
                "El teléfono solo puede contener números y caracteres de formato válido."
            )
        return value

## REPUESTOS 
# Maneja la conversión y validación del modelo Repuesto para la gestión de inventario
class RepuestoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repuesto
        fields = "__all__"

    def validate_codigo_pieza(self, value):
        value = value.strip().upper()  # Forzamos mayúsculas para códigos de pieza (ej: "FIL-123")
        if len(value) < 3:
            raise serializers.ValidationError(
                "El código de la pieza o número de parte debe tener al menos 3 caracteres."
            )
        return value

    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre del repuesto debe tener al menos 3 caracteres."
            )
        return value

    def validate_precio_venta_sugerido(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio de venta sugerido debe ser una cantidad mayor que cero."
            )
        return value

    def validate(self, data):
        # Validación cruzada de negocio entre campos de inventario
        stock_actual = data.get("stock_actual", 0)
        stock_minimo = data.get("stock_minimo", 2)

        if stock_minimo > stock_actual:
            # Esto es opcional, pero es una excelente alerta de negocio para el taller
            pass 

        return data


## METODO DE PAGO SERIALIZER 
# Maneja la conversión y validación del modelo MetodoPago para la caja del taller
class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = "__all__"

    def validate_nombre(self, value):
        value = value.strip()
        
        # Validamos longitud mínima
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre del método de pago debe tener al menos 3 caracteres."
            )
            
        # Opcional: Guardar la primera letra en mayúscula para mantener orden (Efectivo, Tarjeta, etc.)
        return value.capitalize()


##SERVICIO SERIALIZER
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

##ESPECIALIDADES SERIALIZER
# Maneja la conversión y validación del modelo Especialidades para el equipo técnico
class EspecialidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidades
        fields = "__all__"

    def validate_nombre_especialidad(self, value):
        value = value.strip()
        
        # Validación de longitud mínima
        if len(value) < 4:
            raise serializers.ValidationError(
                "El nombre de la especialidad debe tener al menos 4 caracteres."
            )
            
        return value

##ROL DEL SISTEMA SERIALIZER
# Maneja la conversión y validación del modelo RolSistema para la gestión de permisos del taller
class RolSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolSistema
        fields = "__all__"

    def validate_nombre_rol(self, value):
        value = value.strip()

        # Validación de longitud mínima para evitar nombres de rol inválidos
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre del rol debe tener al menos 3 caracteres."
            )

        return value

## ========================================================
## TABLAS CON DEPENDENCIAS DIRECTAS 
## ========================================================

##VEHICULO SERIALIZER 
# Maneja la conversión y validación de los modelos específicos de vehículos vinculados a su marca
class ModeloVehiculoSerializer(serializers.ModelSerializer):
    # Despliega el nombre de la marca en modo de solo lectura (ej: "Toyota")
    marca_nombre = serializers.ReadOnlyField(source="marca.nombre")

    class Meta:
        model = ModeloVehiculo
        fields = "__all__"

    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 1:
            raise serializers.ValidationError(
                "El nombre del modelo de vehículo no puede estar vacío."
            )
        return value

    def validate_tipo_vehiculo(self, value):
        # Validación de seguridad opcional por si envían un tipo fuera de los CHOICES
        formatos_validos = ['AUTO', 'CAMION', 'SUV']
        if value not in formatos_validos:
            raise serializers.ValidationError(
                f"Tipo de vehículo inválido. Opciones permitidas: {', '.join(formatos_validos)}"
            )
        return value

## INVENTARIO DE COMPRA SERIALIZER
# Maneja la conversión y validación de la cabecera de compras a proveedores
class CompraInventarioSerializer(serializers.ModelSerializer):
    # Despliega el nombre comercial de la empresa proveedora en modo de solo lectura
    proveedor_nombre_empresa = serializers.ReadOnlyField(source="proveedor.nombre_empresa")

    class Meta:
        model = CompraInventario
        fields = "__all__"
        # Marcamos total_compra como read_only por redundancia y seguridad en la API
        read_only_fields = ("total_compra", "fecha_compra")

    def validate_numero_factura_proveedor(self, value):
        if value:
            value = value.strip().upper()
            if len(value) < 2:
                raise serializers.ValidationError(
                    "El número de factura del proveedor debe tener al menos 2 caracteres."
                )
        return value

##PERIL DE USUARIO  SERIALIZER 
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    # Trae el nombre legible del rol usando la relación ForeignKey nativa
    rol_nombre = serializers.ReadOnlyField(source="rol.nombre_rol")

    class Meta:
        model = PerfilUsuario
        fields = "__all__"

    def validate_cedula_identidad(self, value):
        if value:
            value = value.strip()
            
            # Validación de longitud mínima estándar
            if len(value) < 5:
                raise serializers.ValidationError(
                    "La cédula de identidad o pasaporte es demasiado corta."
                )
                
            # Validación: Garantizar que sean solo dígitos en la identificación
            if not value.isdigit():
                raise serializers.ValidationError(
                    "La cédula de identidad debe contener únicamente números."
                )
        return value


##MECANICO SERIALIZERS
# Maneja la conversión y validación del modelo Mecanico y su relación ManyToMany
class MecanicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mecanico
        fields = "__all__"

    def validate_nombre(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError(
                "El nombre del mecánico debe tener al menos 3 caracteres."
            )
        return value

    def validate_telefono(self, value):
        if value:
            value = value.strip()
            # Quitamos caracteres de formato comunes para validar que queden solo números
            clean_phone = value.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "")
            
            if not clean_phone.isdigit():
                raise serializers.ValidationError(
                    "El teléfono solo puede contener números."
                )
        return value

    def validate_estado(self, value):
        value = value.lower().strip()
        estados_validos = ["activo", "inactivo"]
        if value not in estados_validos:
            raise serializers.ValidationError(
                "Estado inválido. Las opciones permitidas son 'activo' o 'inactivo'."
            )
        return value


## ========================================================
## VEHÍCULOS Y TRANSACCIONES DEL TALLER 
## ========================================================

##VEHICULO SERIALIZERS (REGISTRA VEHICULO EN EL TALLER )
# Convierte datos del modelo Vehiculo y agrega información del cliente
class VehiculoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")
    modelo_nombre = serializers.ReadOnlyField(source="modelo_vehiculo.nombre")

    class Meta:
        model = Vehiculo
        fields = "__all__"

    def validate_placa(self, value):
        # Limpia espacios sueltos y fuerza mayúsculas (Ej: " pbx-1234 " -> "PBX-1234")
        value = value.strip().upper()
        
        if len(value) < 5:
            raise serializers.ValidationError(
                "La placa del vehículo es demasiado corta."
            )
        return value

    def validate_anio(self, value):
        # Ahora funcionará correctamente gracias a la importación de datetime
        anio_actual = date.today().year

        if value < 1950:
            raise serializers.ValidationError(
                "El año del vehículo no es válido (mínimo 1950)."
            )

        if value > anio_actual + 1:
            raise serializers.ValidationError(
                f"El año del vehículo no puede ser mayor a {anio_actual + 1}."
            )

        return value

## DETALLE COMPRA INVENTARIO SERIALIZER 
class DetalleCompraInventarioSerializer(serializers.ModelSerializer):
    # Campos informativos de solo lectura para el backend
    repuesto_nombre = serializers.ReadOnlyField(source="repuesto.nombre")
    repuesto_codigo = serializers.ReadOnlyField(source="repuesto.codigo_pieza")

    class Meta:
        model = DetalleCompraInventario
        fields = "__all__"
        # Subtotal es editable=False en el modelo, lo marcamos read_only en la API
        read_only_fields = ("subtotal",)

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "La cantidad comprada debe ser como mínimo 1 unidad."
            )
        return value

    def validate_precio_costo_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio de costo unitario debe ser una cantidad mayor a cero."
            )
        return value


##CITAS WEB SERIALIZER
class CitaWebSerializer(serializers.ModelSerializer):
    # Campos de solo lectura para identificar rápidamente al cliente y al auto en consultas
    cliente_nombre = serializers.ReadOnlyField(source="cliente.nombre")
    vehiculo_placa = serializers.ReadOnlyField(source="vehiculo.placa")
    vehiculo_modelo = serializers.ReadOnlyField(source="vehiculo.modelo_vehiculo.nombre")

    class Meta:
        model = CitaWeb
        fields = "__all__"
        # La fecha de creación es automática de Django, por seguridad es read-only
        read_only_fields = ("created_at",)

    def validate_fecha_sugerida(self, value):
        # Valida que la fecha de la cita no esté en el pasado
        # Usamos timezone.now() porque DateTimeField maneja zonas horarias (timezone-aware)
        if value < timezone.now():
            raise serializers.ValidationError(
                "La fecha sugerida para la cita no puede estar en el pasado."
            )
        return value

    def validate_estado(self, value):
        value = value.upper().strip()
        estados_validos = ['SOLICITADA', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA']
        if value not in estados_validos:
            raise serializers.ValidationError(
                f"Estado de cita inválido. Opciones permitidas: {', '.join(estados_validos)}"
            )
        return value

##ORDEN REPARACION SERIALIZER
class OrdenReparacionSerializer(serializers.ModelSerializer):
    vehiculo_placa = serializers.ReadOnlyField(source="vehiculo.placa")

    class Meta:
        model = OrdenReparacion
        fields = "__all__"

    def validate(self, data):
        fecha_salida = data.get("fecha_salida")

        # 1. Si es una actualización (PUT/PATCH), el registro ya existe en la BD
        if self.instance:
            fecha_ingreso = self.instance.fecha_ingreso
        else:
            # 2. Si es una creación (POST), la fecha de ingreso será el "ahora" de Postgres
            fecha_ingreso = timezone.now()

        # 3. Ejecutamos tu validación con la fecha real obtenida
        if fecha_salida and fecha_salida < fecha_ingreso:
            raise serializers.ValidationError(
                {"fecha_salida": "La fecha de salida no puede ser menor que la fecha de ingreso."}
            )

        return data

## ========================================================
## OPERACIONES DE ÓRDENES E HISTORIAL (Nivel 3)
## ========================================================


##DETALLES DE SERVICIO SERIALIZER
class DetalleServicioSerializer(serializers.ModelSerializer):
    # Campos informativos de solo lectura para evitar consultas extras en el backend
    servicio_nombre = serializers.ReadOnlyField(source="servicio.nombre_servicio")
    mecanico_nombre = serializers.ReadOnlyField(source="mecanico.nombre")

    class Meta:
        model = DetalleServicio
        fields = "__all__"
        # Mantienes de forma excelente el subtotal protegido
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


##DETALLES DE ORDEN DE REPUESTOS 
class DetalleRepuestoOrdenSerializer(serializers.ModelSerializer):
    # Campos informativos de solo lectura para el backend
    repuesto_nombre = serializers.ReadOnlyField(source="repuesto.nombre")
    repuesto_codigo = serializers.ReadOnlyField(source="repuesto.codigo_pieza")

    class Meta:
        model = DetalleRepuestoOrden
        fields = "__all__"
        read_only_fields = ("subtotal",)

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "La cantidad de repuestos debe ser al menos 1."
            )
        return value

    def validate_precio_venta_aplicado(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio de venta aplicado debe ser mayor que cero."
            )
        return value

    def create(self, validated_data):
        # Capturamos el ValueError del modelo para que la API responda limpiamente
        try:
            return super().create(validated_data)
        except ValueError as e:
            raise serializers.ValidationError({"cantidad": str(e)})

    def update(self, instance, validated_data):
        # Hacemos lo mismo para el método de actualización (PUT/PATCH)
        try:
            return super().update(instance, validated_data)
        except ValueError as e:
            raise serializers.ValidationError({"cantidad": str(e)})

## FACTURA SERIALIZER
class FacturaSerializer(serializers.ModelSerializer):
    # Campos de solo lectura informativos del cliente y vehículo vinculados a la orden
    cliente_nombre = serializers.ReadOnlyField(source="orden.vehiculo.cliente.nombre")
    vehiculo_placa = serializers.ReadOnlyField(source="orden.vehiculo.placa")

    class Meta:
        model = Factura
        fields = "__all__"
        # El total y la fecha de emisión se manejan de forma estrictamente automática
        read_only_fields = ("total", "fecha_emision")

    def validate_numero_factura(self, value):
        # Limpiamos espacios y estandarizamos el formato
        value = value.strip()
        if len(value) < 5:
            raise serializers.ValidationError(
                "El número de factura es demasiado corto para cumplir con los estándares contables."
            )
        return value

    def validate_subtotal(self, value):
        if value < 0:
            raise serializers.ValidationError("El subtotal no puede ser una cantidad negativa.")
        return value

    def validate_impuesto(self, value):
        if value < 0:
            raise serializers.ValidationError("El valor de los impuestos no puede ser una cantidad negativa.")
        return value

    def validate(self, data):
        # Lógica cruzada para calcular automáticamente el total de la factura
        # Soportamos tanto creación (POST) como actualizaciones parciales (PATCH)
        subtotal = data.get("subtotal") if "subtotal" in data else (self.instance.subtotal if self.instance else 0)
        impuesto = data.get("impuesto") if "impuesto" in data else (self.instance.impuesto if self.instance else 0)

        # Inyectamos el cálculo matemático antes de que llegue a PostgreSQL
        data["total"] = subtotal + impuesto
        return data

##REGISTRO DE PAGO SERIALIZER 
class RegistroPagoSerializer(serializers.ModelSerializer):
    # Campos informativos útiles para auditar el pago desde el backend
    factura_numero = serializers.ReadOnlyField(source="factura.numero_factura")
    metodo_pago_nombre = serializers.ReadOnlyField(source="metodo_pago.nombre_metodo")

    class Meta:
        model = RegistroPago
        fields = "__all__"
        read_only_fields = ("fecha_pago",)

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto del pago debe ser estrictamente mayor a cero.")
        return value

    def validate(self, data):
        factura = data.get("factura")
        monto_nuevo_pago = data.get("monto")

        # Contexto para soportar POST y evitar fallos si es una actualización parcial
        if not factura and self.instance:
            factura = self.instance.factura
        if not monto_nuevo_pago and self.instance:
            monto_nuevo_pago = self.instance.monto

        # 1. Calcular cuánto se ha pagado de esta factura hasta ahora
        pagos_previos = factura.pagos.all()
        
        # Si estamos editando (PUT/PATCH), excluimos el monto anterior de este mismo pago
        if self.instance:
            pagos_previos = pagos_previos.exclude(id=self.instance.id)
            
        total_pagado_anteriormente = sum(pago.monto for pago in pagos_previos)
        saldo_pendiente = factura.total - total_pagado_anteriormente

        # 2. Regla de negocio: No se puede pagar más de lo que se debe
        if monto_nuevo_pago > saldo_pendiente:
            raise serializers.ValidationError(
                {"monto": f"Monto excedido. El saldo pendiente de esta factura es de ${saldo_pendiente}."}
            )

        # 3. Guardamos temporalmente en el contexto de validación si este pago liquida la factura
        # Redondeamos a 2 decimales para evitar problemas de precisión de punto flotante
        if round(monto_nuevo_pago, 2) == round(saldo_pendiente, 2):
            data["_liquidar_factura"] = True
        else:
            data["_liquidar_factura"] = False

        return data

    def create(self, validated_data):
        # Extraemos la bandera interna antes de crear el registro
        liquidar = validated_data.pop("_liquidar_factura", False)
        
        # Creamos el registro de pago de forma normal en PostgreSQL
        pago = super().create(validated_data)
        
        # Si el pago liquida el total, actualizamos la tabla Factura de forma automática
        if liquidar:
            factura = pago.factura
            factura.paged = True  # Cambiamos el estado a pagada
            factura.pagada = True
            factura.save()
            
        return pago












