from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Lectura para cualquiera.
    Crear/actualizar/eliminar solo para usuarios staff (admin).
    """
#Protege las rutas del admin y permite hacer get a usuarios sin  autenticar
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)
