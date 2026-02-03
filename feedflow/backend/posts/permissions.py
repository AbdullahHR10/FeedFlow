"""
Permissions for post-related views.

Includes:
- IsPostAuthor: Gives proper permissions to the users.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPostAuthor(BasePermission):
    """Allows write access to author and staff.
    Allows read-only access to everyone."""
    def has_object_permission(self, request, view, obj):
        """Checks if the user has object permission."""
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user or not user.is_authenticated:
            return False

        return user.is_staff or obj.author == user
