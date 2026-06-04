from django.contrib import admin
from .models import Cliente, Vehiculo, Mecanico, Servicio, DetalleServicio, OrdenReparacion

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Mecanico)
admin.site.register(Servicio)
admin.site.register(OrdenReparacion)
admin.site.register(DetalleServicio)