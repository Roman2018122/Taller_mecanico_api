from django.db import models
from django.core.validators import MinValueValidator



class Cliente (models.Model):
    nombre = models.CharField(max_length = 200)
    telefono  = models.CharField(max_length= 15)
    correo =  models.CharField(max_length= 100)
    direccion = models.CharField(max_length =  200)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self. nombre} ({self.id})"
    


class Vehiculo (models.Model):
    marca = models.CharField(max_length = 50)
    placa = models.CharField(max_length = 10)
    modelo = models.CharField(max_length = 50)
    anio =  models.PositiveIntegerField()
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE, ## elimina sus vehiculos si se elimina a el cliente
        related_name="vehiculos",

    )
    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

class Servicio(models.Model):
    nombre = models.CharField(max_length = 100)
    descripcion= models.TextField(blank=True, null= True )
    precio_referencial = models.DecimalField(
        max_digits= 10,
        decimal_places= 2,
        validators=[MinValueValidator(0)], ## Valida que un campo no tenga valor menor que 0
    )
    def __str__(self):
        return self.nombre
    

    
class Mecanico(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    id_mecanico = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    especialidad = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default="activo",
    )
    def __str__(self):
        return self.nombre
    
class OrdenReparacion(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("finalizado", "Finalizado"),
    ]

    id_orden = models.AutoField(primary_key=True)
    vehiculo = models.ForeignKey(
        Vehiculo,
        on_delete=models.CASCADE,
        related_name="ordenes",
    )
    mecanico = models.ForeignKey(
        Mecanico,
        on_delete=models.SET_NULL,
        related_name="ordenes",
        null=True,
        blank=True,
    )
    fecha_ingreso = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="pendiente",
    )
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden #{self.id_orden} - {self.vehiculo.placa}"
    

    


class DetalleServicio(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    orden = models.ForeignKey(
        OrdenReparacion,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        related_name="detalles",
    )
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcula subtotal automaticamente si no viene
        if self.precio_unitario is not None and self.cantidad is not None:
            self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id_detalle} - Orden {self.orden_id}"

    
    


