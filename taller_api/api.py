from rest_framework import viewsets, permissions 
from rest_framework import permissions as drf_permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly


from .models import (Cliente, Vehiculo, Servicio, Mecanico, OrdenReparacion, DetalleServicio )
from .serializers import (
    ClienteSerializer, 
    VehiculoSerializer, 
    ServicioSerializer, 
    MecanicoSerializer,
    OrdenReparacionSerializer, 
    DetalleServicioSerializer
    )


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by("id")
    permission_classes = [permissions.AllowAny] ## cambiar si se necesita estar autenticado
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]## Proteccion de ruta
    search_fields = ["nombre", "telefono", "correo"]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.select_related("cliente").all().order_by("id")
    serializer_class = VehiculoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["placa", "marca", "modelo", "cliente__nombre"]

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all().order_by("id")
    serializer_class = ServicioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["nombre", "descripcion"]

class MecanicoViewSet(viewsets.ModelViewSet):
    queryset = Mecanico.objects.all().order_by("id_mecanico")
    serializer_class = MecanicoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["nombre", "especialidad", "estado"]

class OrdenReparacionViewSet(viewsets.ModelViewSet):
    queryset = (
        OrdenReparacion.objects
        .select_related("vehiculo", "mecanico")
        .all()
        .order_by("-fecha_ingreso")
    )
    serializer_class = OrdenReparacionSerializer
    search_fields = ["vehiculo__placa", "estado", "mecanico__nombre"]
    
    authentication_classes = [] 
    permission_classes = [IsAdminOrReadOnly]

    # Agregamos esto para estar 100% seguros de que DRF no pida nada
    def get_permissions(self):
        return [drf_permissions.AllowAny()]

class DetalleServicioViewSet(viewsets.ModelViewSet):
    queryset = (
        DetalleServicio.objects
        .select_related("orden", "servicio")
        .all()
        .order_by("id_detalle")
    )
    serializer_class = DetalleServicioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["orden__id_orden", "servicio__nombre"]


