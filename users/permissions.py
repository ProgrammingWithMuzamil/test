from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows public read access (GET) and admin-only write access (POST/PUT/DELETE).
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Public access for GET, HEAD, OPTIONS
        
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsAdminOrSelf(permissions.BasePermission):
    """
    Allows access only if user is admin or accessing their own data.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        # Allow users to view and edit their own profile
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin_role


class IsAdminRole(permissions.BasePermission):
    """
    Allows access only to users with admin role.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin_role


class IsAgentRole(permissions.BasePermission):
    """
    Allows access only to users with agent role.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_agent_role


class IsAdminOrAgentRole(permissions.BasePermission):
    """
    Allows access to users with admin or agent role.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin_role or request.user.is_agent_role)
        )


class IsAdminOnly(permissions.BasePermission):
    """
    Allows access only to admin users, explicitly blocking agents.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_admin_role and 
            not request.user.is_agent_role
        )
