from rest_framework import viewsets, permissions 
from rest_framework import permissions as drf_permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly


from .models import (
    ##Modulo1
    Cliente, Marca, Proveedor, Repuesto, MetodoPago, Servicio, Especialidades, RolSistema, 
    ##Modulo2 
    ModeloVehiculo, CompraInventario, PerfilUsuario, Mecanico, 
    ##modulo3
    Vehiculo, DetalleCompraInventario, CitaWeb, OrdenReparacion,
    ##Modulo4
    DetalleServicio, DetalleRepuestoOrden, Factura, RegistroPago

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
    FacturaSerializer, RegistroPagoSerializer )

# ========================================================
# VISTAS: MÓDULO 1 - TABLAS BASE INDEPENDIENTES
# ========================================================
class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para la gestión de Clientes.
    Permite buscar por nombre, teléfono o correo.
    """
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre', 'telefono', 'correo']


class MarcaViewSet(viewsets.ModelViewSet):
    """
    CRUD para las Marcas de vehículos y repuestos.
    """
    queryset = Marca.objects.all().order_by('id')
    serializer_class = MarcaSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['nombre']


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
    queryset = ModeloVehiculo.objects.select_related('marca').all().order_by('id')
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
    Optimizado para traer los datos del cliente y el modelo en una sola consulta SQL.
    """
    queryset = Vehiculo.objects.select_related('modelo_vehiculo__marca', 'cliente').all().order_by('id')
    serializer_class = VehiculoSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['placa', 'cliente__nombre', 'modelo_vehiculo__nombre']


class DetalleCompraInventarioViewSet(viewsets.ModelViewSet):
    """
    Control operativo de las piezas que ingresan en una Compra de Inventario.
    """
    queryset = DetalleCompraInventario.objects.select_related('compra', 'repuesto').all().order_by('id')
    serializer_class = DetalleCompraInventarioSerializer
    permission_classes = [IsAdminOrReadOnly]


class CitaWebViewSet(viewsets.ModelViewSet):
    """
    Gestión de Citas solicitadas por los clientes vía web.
    """
    queryset = CitaWeb.objects.select_related('cliente', 'vehiculo__modelo_vehiculo').all().order_by('-fecha_sugerida')
    serializer_class = CitaWebSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['cliente__nombre', 'vehiculo__placa', 'estado']


class OrdenReparacionViewSet(viewsets.ModelViewSet):
    """
    Cabecera principal de Órdenes de Reparación en el taller.
    """
    queryset = OrdenReparacion.objects.select_related('vehiculo__cliente').all().order_by('-fecha_ingreso')
    serializer_class = OrdenReparacionSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['id', 'vehiculo__placa', 'estado']


# ========================================================
# VISTAS: MÓDULO 4 - OPERACIONES DE ÓRDENES E HISTORIAL
# ========================================================

class DetalleServicioViewSet(viewsets.ModelViewSet):
    """
    CRUD para los servicios/mano de obra aplicados a una orden.
    Optimizado con select_related para traer la orden, el servicio y el mecánico asignado.
    """
    queryset = DetalleServicio.objects.select_related('orden', 'servicio', 'mecanico').all().order_by('id')
    serializer_class = DetalleServicioSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['orden__id', 'servicio__nombre', 'mecanico__nombre']


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

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer