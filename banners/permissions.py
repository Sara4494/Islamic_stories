from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnlyForAuthenticated(BasePermission):
    """
    - لو request.method في SAFE_METHODS (GET, HEAD, OPTIONS):
        => مسموح لأي user يكون عامل login أو admin
    - باقي الميثودز (POST, PUT, PATCH, DELETE):
        => مسموح للـ admin بس
    """
    def has_permission(self, request, view):
        # السماح بالـ GET للي عامل login أو admin
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # باقي العمليات للـ admin فقط
        return request.user and request.user.is_staff
