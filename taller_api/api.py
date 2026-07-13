from rest_framework import viewsets, permissions 
from rest_framework import permissions as drf_permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

from django.db.models.deletion import ProtectedError
from rest_framework.response import Response
from rest_framework import status


from .models import (
    ##Modulo1
    Cliente, Marca, Proveedor, Repuesto, MetodoPago, Servicio, Especialidades, RolSistema, 
    ##Modulo2 
    ModeloVehiculo, CompraInventario, PerfilUsuario, Mecanico, 
    ##modulo3
    Vehiculo, DetalleCompraInventario, CitaWeb, OrdenReparacion,
    ##Modulo4
    DetalleServicio, DetalleRepuestoOrden, Factura, RegistroPago,

    
    )
from .serializers import (
    ##Modulo1
    ClienteSerializer,  MarcaSerializer,ProveedorSerializer, RepuestoSerializer,
    MetodoPagoSerializer,ServicioSerializer, EspecialidadesSerializer,RolSistemaSerializer,
    ##Modulo2
    ModeloVehiculoSerializer, CompraInventarioSerializer, 
    PerfilUsuarioSerializer, MecanicoSerializer,
    ##Modulo3
    VehiculoSerializer, DetalleCompraInventarioSerializer, 
    CitaWebSerializer, OrdenReparacionSerializer,
    ##Modulo4
    DetalleServicioSerializer, DetalleRepuestoOrdenSerializer, 
    FacturaSerializer, RegistroPagoSerializer, 
    
    RegistroClienteSerializer, )

    
    
# ========================================================
# VISTAS: MÓDULO 1 - TABLAS BASE INDEPENDIENTES
# ========================================================
class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de Clientes.
    Permite buscar por nombre, teléfono o correo.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre', 'telefono', 'correo']
    filterset_fields = ["created_at"]
    ordering_fields = ["nombre"]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError:
            return Response(
                {   
                    "detail": (
                        "No se puede eliminar este cliente porque tiene "
                        "vehículos registrados."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class MarcaViewSet(viewsets.ModelViewSet):
    """
    CRUD para las Marcas de vehículos y repuestos.
    """
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre']
    ordering_fields = [
    "nombre"
    ]

class ProveedorViewSet(viewsets.ModelViewSet):
    """
    Gestión de Proveedores de repuestos.
    Búsquedas optimizadas por RUC/NIT o Nombre de Empresa.
    """
    queryset = Proveedor.objects.all().order_by('id')
    serializer_class = ProveedorSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre_empresa', 'ruc_nit', 'contacto_nombre']


class RepuestoViewSet(viewsets.ModelViewSet):
    """
    Control de catálogo e inventario físico de Repuestos.
    Permite localizar piezas de inmediato por su código de fábrica o nombre.
    """
    queryset = Repuesto.objects.all().order_by('id')
    serializer_class = RepuestoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['codigo_pieza', 'nombre']


class MetodoPagoViewSet(viewsets.ModelViewSet):
    """
    Catálogo de métodos de pago activos en la caja del taller.
    """
    queryset = MetodoPago.objects.all().order_by('id')
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre']


class ServicioViewSet(viewsets.ModelViewSet):
    """
    Catálogo de mano de obra y servicios disponibles.
    """
    queryset = Servicio.objects.all().order_by('id')
    serializer_class = ServicioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = [
    "nombre",
    "precio_referencial"
    ]


class EspecialidadesViewSet(viewsets.ModelViewSet):
    """
    Especialidades asignables al personal técnico del taller.
    """
    queryset = Especialidades.objects.all().order_by('id')
    serializer_class = EspecialidadesSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre_especialidad']


class RolSistemaViewSet(viewsets.ModelViewSet):
    """
    Roles disponibles para la definición de permisos y perfiles de usuarios.
    """
    queryset = RolSistema.objects.all().order_by('id')
    serializer_class = RolSistemaSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre_rol']


# ========================================================
# VISTAS: MÓDULO 2 - TABLAS CON DEPENDENCIAS DIRECTAS 
# ========================================================

class ModeloVehiculoViewSet(viewsets.ModelViewSet):
    """
    CRUD para los Modelos de Vehículos.
    Optimizado con select_related para traer la Marca asociada de inmediato.
    """
    queryset = ModeloVehiculo.objects.select_related('marca').all()
    serializer_class = ModeloVehiculoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre', 'marca__nombre', 'tipo_vehiculo']



class CompraInventarioViewSet(viewsets.ModelViewSet):
    """
    Control de las cabeceras de compras de inventario a Proveedores.
    """
    queryset = CompraInventario.objects.select_related('proveedor').all().order_by('-fecha_compra')
    serializer_class = CompraInventarioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['numero_factura_proveedor', 'proveedor__nombre_empresa']


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    """
    Gestión de Perfiles de Usuario extendidos del sistema del taller.
    """
    queryset = PerfilUsuario.objects.select_related('usuario', 'rol').all().order_by('id')
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['usuario__username', 'rol__nombre_rol', 'cedula_identidad']


class MecanicoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Mecánicos.
    Optimizado con prefetch_related para la relación ManyToMany de sus especialidades.
    """
    queryset = Mecanico.objects.prefetch_related('especialidades').all().order_by('id')
    serializer_class = MecanicoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre', 'estado']


# ========================================================
# VISTAS: MÓDULO 3 - VEHÍCULOS Y TRANSACCIONES DEL TALLER
# ========================================================

class VehiculoViewSet(viewsets.ModelViewSet):
    """
    CRUD completo de Vehículos.
    Optimizado para traer el cliente y el modelo del vehículo en una sola consulta.
    """
    queryset = Vehiculo.objects.select_related(
        "cliente",
        "modelo_vehiculo",
        "modelo_vehiculo__marca"
    ).all().order_by("id")

    serializer_class = VehiculoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = [
        "placa",
        "cliente__nombre",
        "modelo_vehiculo__nombre",
        "modelo_vehiculo__marca__nombre",
    ]


class DetalleCompraInventarioViewSet(viewsets.ModelViewSet):
    """
    Control operativo de las piezas que ingresan en una Compra de Inventario.
    """
    queryset = DetalleCompraInventario.objects.select_related('compra', 'repuesto').all().order_by('id')
    serializer_class = DetalleCompraInventarioSerializer
    permission_classes = [IsAdminOrReadOnly]


class CitaWebViewSet(viewsets.ModelViewSet):
    """
    Gestión de Citas solicitadas por los clientes.
    Optimizado para traer el cliente y el vehículo en una sola consulta.
    """
    queryset = CitaWeb.objects.select_related(
        "cliente",
        "vehiculo",
        "vehiculo__modelo_vehiculo",
        "vehiculo__modelo_vehiculo__marca"
    ).all().order_by("-fecha_sugerida")

    serializer_class = CitaWebSerializer
    permission_classes = [IsAdminOrReadOnly]

    search_fields = [
        "cliente__nombre",
        "vehiculo__placa",
        "vehiculo__modelo_vehiculo__nombre",
        "estado",
    ]


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class OrdenReparacionViewSet(viewsets.ModelViewSet):
    """
    Cabecera principal de órdenes de reparación del taller.
    """
    queryset = OrdenReparacion.objects.select_related(
        "vehiculo",
        "vehiculo__cliente",
        "vehiculo__modelo_vehiculo",
        "vehiculo__modelo_vehiculo__marca",
    ).order_by("-fecha_ingreso")

    serializer_class = OrdenReparacionSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "vehiculo__placa",
        "vehiculo__cliente__nombre",
        "vehiculo__modelo_vehiculo__nombre",
        "estado",
    ]

    filterset_fields = [
        "estado",
        "vehiculo",
    ]

    ordering_fields = [
        "fecha_ingreso",
        "fecha_salida",
        "estado",
    ]


# ========================================================
# VISTAS: MÓDULO 4 - OPERACIONES DE ÓRDENES E HISTORIAL
# ========================================================

class DetalleServicioViewSet(viewsets.ModelViewSet):
    """
    CRUD para los servicios aplicados a una orden.
    """
    queryset = DetalleServicio.objects.select_related(
        "orden",
        "orden__vehiculo",
        "orden__vehiculo__cliente",
        "servicio",
        "mecanico",
    ).order_by("id")

    serializer_class = DetalleServicioSerializer
    permission_classes = [IsAdminOrReadOnly]

    search_fields = [
        "orden__vehiculo__placa",
        "servicio__nombre",
        "mecanico__nombre",
    ]

    ordering_fields = [
        "cantidad",
        "precio_unitario",
        "subtotal",
    ]


class DetalleRepuestoOrdenViewSet(viewsets.ModelViewSet):
    """
    Control de los repuestos cargados a las órdenes de reparación.
    Maneja el descuento automático de inventario físico.
    """
    queryset = DetalleRepuestoOrden.objects.select_related('orden', 'repuesto').all().order_by('id')
    serializer_class = DetalleRepuestoOrdenSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['orden__id', 'repuesto__nombre', 'repuesto__codigo_pieza']


class FacturaViewSet(viewsets.ModelViewSet):
    """
    Gestión de facturación del taller.
    Calcula de forma automática el total (subtotal + impuesto) antes del guardado.
    """
    queryset = Factura.objects.select_related('orden__vehiculo__cliente').all().order_by('-fecha_emision')
    serializer_class = FacturaSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['numero_factura', 'orden__id', 'orden__vehiculo__cliente__nombre']


class RegistroPagoViewSet(viewsets.ModelViewSet):
    """
    Control de caja y pagos recibidos para las facturas.
    Valida saldos pendientes y cambia el estado de la factura a PAGADA automáticamente.
    """
    queryset = RegistroPago.objects.select_related('factura', 'metodo_pago').all().order_by('-fecha_pago')
    serializer_class = RegistroPagoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['factura__numero_factura', 'comprobante_referencia']


##SERIALIZADOR
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# 🚀 Importas el serializer que acabamos de mover a serializers.py
from .serializers import RegistroClienteSerializer 

class RegistroClienteView(APIView):
    # Permite que cualquier persona se registre sin mandar Token de seguridad
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = RegistroClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Cliente registrado con éxito y rol asignado"}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


