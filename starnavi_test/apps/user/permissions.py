from rest_framework.permissions import BasePermission

class UserPermissions(BasePermission):
    """
    Handles permissions for users.  The basic rules are

     - owner may GET, PUT, POST, DELETE
     - nobody else can access
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # check if user is owner
        return request.user == obj.user or request.user.is_staff
