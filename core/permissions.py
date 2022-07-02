from rest_framework.permissions import BasePermission

class IsAnonOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user_type = view.kwargs.get('user_type')
        if user_type == 'user':
            return True
        elif user_type == 'staff':
            return request.auth and request.user.is_staff
        else:
            return False