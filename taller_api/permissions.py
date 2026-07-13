from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Lectura para cualquiera.
    Crear/actualizar/eliminar solo para usuarios staff (admin).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)



class IsAdminUserRole(BasePermission):
    """
    Para el Administrador del taller.
    Bloquea por completo el acceso a cualquier cliente (ni lectura, ni escritura).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol.nombre_rol.lower() == 'administrador'
        )

class IsClienteUserRole(BasePermission):
    """
    Para los Clientes registrados.
    Bloquea el acceso a administradores o usuarios anónimos en rutas específicas.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol.nombre_rol.lower() == 'cliente'
        )