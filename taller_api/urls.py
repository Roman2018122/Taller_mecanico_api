from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView, 
)

# Importación de todas mis vistas de api.py
from .api import (
    # Módulo 1
    ClienteViewSet, MarcaViewSet,  
    ServicioViewSet, EspecialidadesViewSet, RolSistemaViewSet,
    
    # Módulo 2
    ModeloVehiculoViewSet,  PerfilUsuarioViewSet, MecanicoViewSet,
    
    # Módulo 3
    VehiculoViewSet,  CitaWebViewSet, OrdenReparacionViewSet,
    
    # Módulo 4
    DetalleServicioViewSet, 

    RegistroClienteView,

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

router.register(r'servicios', ServicioViewSet, basename='servicio')
router.register(r'especialidades', EspecialidadesViewSet, basename='especialidades')
router.register(r'roles-sistema', RolSistemaViewSet, basename='rolsistema')

# Módulo 2
router.register(r'modelos-vehiculo', ModeloVehiculoViewSet, basename='modelovehiculo')
router.register(r'perfiles-usuario', PerfilUsuarioViewSet, basename='perfilusuario')
router.register(r'mecanicos', MecanicoViewSet, basename='mecanico')

# Módulo 3
router.register(r'vehiculos', VehiculoViewSet, basename='vehiculo')
router.register(r'citas-web', CitaWebViewSet, basename='citaweb')
router.register(r'ordenes-reparacion', OrdenReparacionViewSet, basename='ordenreparacion')

# Módulo 4
router.register(r'detalles-servicio', DetalleServicioViewSet, basename='detalleservicio')

# ========================================================
# ESTRUCTURA DE RUTAS DE LA API
# ========================================================
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Agregas la ruta pública para registrarse
    path('api/registro/', RegistroClienteView.as_view(), name='registro_publico'),
]