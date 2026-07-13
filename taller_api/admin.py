from django.contrib import admin
from .models import Cliente, Vehiculo, Mecanico, Servicio, DetalleServicio, OrdenReparacion, RolSistema, PerfilUsuario

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Mecanico)
admin.site.register(Servicio)
admin.site.register(OrdenReparacion)
admin.site.register(DetalleServicio)

## Sistema roles
admin.site.register(RolSistema)
admin.site.register(PerfilUsuario)