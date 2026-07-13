from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

## ========================================================
## MÓDULO 1: TABLAS BASE INDEPENDIENTES (Sin dependencias)
## ========================================================

from django.contrib.auth.models import User


class Cliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="cliente",
        null=True,
        blank=True,
    )

    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(max_length=100)
    direccion = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.id})"
    
   


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    pais_origen = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
    
    


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=150, unique=True)
    ruc_nit = models.CharField(max_length=20, unique=True, help_text="Identificación fiscal")
    contacto_nombre = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nombre_empresa


class Repuesto(models.Model):
    codigo_pieza = models.CharField(max_length=50, unique=True, help_text="Número de parte de fábrica")
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio_venta_sugerido = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_actual = models.PositiveIntegerField(default=0, help_text="Cantidad física disponible en taller")
    stock_minimo = models.PositiveIntegerField(default=2, help_text="Alerta cuando el inventario baje de este número")

    def __str__(self):
        return f"{self.codigo_pieza} - {self.nombre} (Stock: {self.stock_actual})"


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Efectivo, Transferencia, Tarjeta")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio_referencial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Especialidades(models.Model):
    nombre_especialidad = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    esta_activa = models.BooleanField(default=True) 
    
    def __str__(self):
        return f"{self.nombre_especialidad} ({self.id})"


class RolSistema(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True, help_text="Ej: Administrador, Recepcionista, Jefe de Taller")
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre_rol


## ========================================================
## MÓDULO 2: TABLAS CON DEPENDENCIAS DIRECTAS (Nivel 1)
## ========================================================

class ModeloVehiculo(models.Model): 
    TIPO_VEHICULO_CHOICES = [
        ('AUTO', 'Automóvil / Carro'),
        ('CAMION', 'Camión'),
        ('SUV', 'Camioneta / SUV'),
    ]

    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name='modelos')
    nombre = models.CharField(max_length=60)
    tipo_vehiculo = models.CharField(max_length=15, choices=TIPO_VEHICULO_CHOICES, default='AUTO')
    
    class Meta:
        unique_together = ["marca", "nombre"]
        ordering = ["marca__nombre", "nombre"]

    def __str__(self):
        return f"{self.marca.nombre} {self.nombre}"


class CompraInventario(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name="compras")
    fecha_compra = models.DateTimeField(auto_now_add=True)
    numero_factura_proveedor = models.CharField(max_length=50, blank=True, null=True)
    total_compra = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)

    def __str__(self):
        return f"Compra #{self.id} - {self.proveedor.nombre_empresa}"


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.ForeignKey(RolSistema, on_delete=models.PROTECT, related_name="usuarios")
    cedula_identidad = models.CharField(max_length=20, unique=True, blank=True, null=True)
    esta_disponible = models.BooleanField(default=True, help_text="Para asignación de tareas en el taller")

    def __str__(self):
        return f"{self.usuario.username} - {self.rol.nombre_rol}"
    
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def crear_perfil_usuario_automatico(sender, instance, created, **kwargs):
    if created:
        # 1. Si el usuario es el superusuario supremo de la terminal, le ponemos Administrador
        if instance.is_superuser:
            rol_admin, _ = RolSistema.objects.get_or_create(
                nombre_rol="Administrador", 
                defaults={"descripcion": "Acceso total al taller"}
            )
            PerfilUsuario.objects.get_or_create(usuario=instance, rol=rol_admin)
        
        # 2. 🚀 PARA CUALQUIER OTRO USUARIO NUEVO: Nace siendo Cliente por defecto
        else:
            rol_cliente, _ = RolSistema.objects.get_or_create(
                nombre_rol="Cliente", 
                defaults={"descripcion": "Usuario dueño de vehículos"}
            )
            PerfilUsuario.objects.get_or_create(usuario=instance, rol=rol_cliente)




class Mecanico(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="activo")
    especialidades = models.ManyToManyField(Especialidades, related_name="mecanicos", blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


## ========================================================
## MÓDULO 3: VEHÍCULOS Y TRANSACCIONES DEL TALLER (Nivel 2)
## ========================================================

class Vehiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo_vehiculo = models.ForeignKey(
        ModeloVehiculo, 
        on_delete=models.PROTECT, 
        related_name="unidades_vehiculos"
    )    
    anio = models.PositiveIntegerField()
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="vehiculos",
    )
    color = models.CharField(
        max_length=30,
        blank=True
    )
    kilometraje = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.placa} - {self.modelo_vehiculo} ({self.anio})"


class DetalleCompraInventario(models.Model):
    compra = models.ForeignKey(CompraInventario, on_delete=models.CASCADE, related_name="detalles")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT, related_name="detalles_compras")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_costo_unitario
        super().save(*args, **kwargs)
        self.repuesto.stock_actual += self.cantidad
        self.repuesto.save()


class CitaWeb(models.Model):
    ESTADO_CITA_CHOICES = [
        ('SOLICITADA', 'Solicitada / Pendiente'),
        ('CONFIRMADA', 'Confirmada por el Taller'),
        ('EN_PROCESO', 'En proceso'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Asistió / Convertida en Orden'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="citas")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name="citas")
    fecha_sugerida = models.DateTimeField(help_text="Fecha y hora que el cliente desea asistir")
    motivo_consulta = models.TextField(help_text="Breve descripción de lo que le pasa al vehículo")
    estado = models.CharField(max_length=20, choices=ESTADO_CITA_CHOICES, default='SOLICITADA')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cita #{self.id} - {self.cliente.nombre} ({self.fecha_sugerida.date()})"


class OrdenReparacion(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("finalizado", "Finalizado"),
    ]
    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="ordenes")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="pendiente")
    observaciones = models.TextField(blank=True, null=True)
    mecanico_responsable = models.ForeignKey(
        Mecanico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Orden #{self.id} - {self.vehiculo.placa}"


## ========================================================
## MÓDULO 4: OPERACIONES DE ÓRDENES E HISTORIAL (Nivel 3)
## ========================================================

class DetalleServicio(models.Model):
    orden = models.ForeignKey(OrdenReparacion, on_delete=models.CASCADE, related_name="detalles")
    servicio = models.ForeignKey(Servicio, on_delete=models.PROTECT, related_name="detalles")
    mecanico = models.ForeignKey(Mecanico, on_delete=models.PROTECT, related_name="detalles_servicios", null=True)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        if self.precio_unitario is not None and self.cantidad is not None:
            self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle #{self.id} - Orden #{self.orden.id}"


class DetalleRepuestoOrden(models.Model):
    orden = models.ForeignKey(OrdenReparacion, on_delete=models.CASCADE, related_name="detalles_repuestos")
    repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT, related_name="detalles_ordenes")
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_venta_aplicado = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_venta_aplicado
        super().save(*args, **kwargs)
        
        if self.repuesto.stock_actual >= self.cantidad:
            self.repuesto.stock_actual -= self.cantidad
            self.repuesto.save()
        else:
            raise ValueError(f"No hay suficiente stock para {self.repuesto.nombre}")


class Factura(models.Model):
    orden = models.OneToOneField(
        OrdenReparacion, 
        on_delete=models.PROTECT, 
        related_name="factura",
        help_text="Una orden solo puede tener una factura"
    )
    numero_factura = models.CharField(max_length=20, unique=True, help_text="Ej: 001-001-000001")
    fecha_emision = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="IVA / Tax")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pagada = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura {self.numero_factura} (Total: ${self.total})"


class RegistroPago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="pagos")
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    fecha_pago = models.DateTimeField(auto_now_add=True)
    comprobante_referencia = models.CharField(max_length=100, blank=True, null=True, help_text="Número de depósito o voucher")

    def __str__(self):
        return f"Pago a Factura {self.factura.numero_factura} por ${self.monto}"
    

