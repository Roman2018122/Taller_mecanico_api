from rest_framework import routers

from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



from .api import  ClienteViewSet
from .api import VehiculoViewSet
from .api import ServicioViewSet
from .api import MecanicoViewSet
from .api import OrdenReparacionViewSet
from .api import DetalleServicioViewSet

router = routers.DefaultRouter()

router.register('api/Cliente', ClienteViewSet, 'clientes')
router.register('api/Vehiculo', VehiculoViewSet, 'vehiculos' )
router.register('api/Servicio', ServicioViewSet,  'servicios')
router.register('api/Mecanico', MecanicoViewSet,  'mecanico')
router.register('api/OrdenReparacion', OrdenReparacionViewSet, 'ordenReparacion')
router.register('api/DetalleServicio', DetalleServicioViewSet, 'detalleServicio')


urlpatterns = [
    path('', include(router.urls)),

    path(
        'api/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]