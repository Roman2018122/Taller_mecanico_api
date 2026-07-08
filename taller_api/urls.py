from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView, # Dejamos solo la de refrescar tokens de la librería nativa
)

# Importación de todas tus vistas (ViewSets) de api.py
from .api import (
    # Módulo 1
    ClienteViewSet, MarcaViewSet, ProveedorViewSet, RepuestoViewSet,
    MetodoPagoViewSet, ServicioViewSet, EspecialidadesViewSet, RolSistemaViewSet,
    
    # Módulo 2
    ModeloVehiculoViewSet, CompraInventarioViewSet, PerfilUsuarioViewSet, MecanicoViewSet,
    
    # Módulo 3
    VehiculoViewSet, DetalleCompraInventarioViewSet, CitaWebViewSet, OrdenReparacionViewSet,
    
    # Módulo 4
    DetalleServicioViewSet, DetalleRepuestoOrdenViewSet, FacturaViewSet, RegistroPagoViewSet,

    # 🛠️ IMPLEMENTACIÓN: Importamos tu nueva vista personalizada desde api.py
    CustomTokenObtainPairView
)

# Inicializamos el DefaultRouter
router = routers.DefaultRouter()

# ========================================================
# REGISTRO DE ENDPOINTS EN EL ROUTER
# ========================================================
# Módulo 1
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'marcas', MarcaViewSet, basename='marca')
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')
router.register(r'repuestos', RepuestoViewSet, basename='repuesto')
router.register(r'metodos-pago', MetodoPagoViewSet, basename='metodopago')
router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'especialidades', EspecialidadesViewSet, basename='especialidades')
router.register(r'roles-sistema', RolSistemaViewSet, basename='rolsistema')

# Módulo 2
router.register(r'modelos-vehiculo', ModeloVehiculoViewSet, basename='modelovehiculo')
router.register(r'compras-inventario', CompraInventarioViewSet, basename='comprainventario')
router.register(r'perfiles-usuario', PerfilUsuarioViewSet, basename='perfilusuario')
router.register(r'mecanicos', MecanicoViewSet, basename='mecanico')

# Módulo 3
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'detalles-compra', DetalleCompraInventarioViewSet, basename='detallecomprainventario')
router.register(r'citas-web', CitaWebViewSet, basename='citaweb')
router.register(r'ordenes-reparacion', OrdenReparacionViewSet, basename='ordenreparacion')

# Módulo 4
router.register(r'detalles-servicio', DetalleServicioViewSet, basename='detalleservicio')
router.register(r'detalles-repuesto', DetalleRepuestoOrdenViewSet, basename='detallerepuestoorden')
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'registros-pago', RegistroPagoViewSet, basename='registropago')


# ========================================================
# ESTRUCTURA FINAL DE RUTAS DE LA API
# ========================================================
urlpatterns = [
    # Agrupa todos los endpoints del router bajo el prefijo api/v1/
    path('api/v1/', include(router.urls)),

    # 🛠️ IMPLEMENTACIÓN: Usamos tu CustomTokenObtainPairView en lugar de TokenObtainPairView
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]