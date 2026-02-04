"""
Permissions for post-related views.

Includes:
- isOwnerOrStaff: Gives proper permissions on an object to the users.
- IsPostAuthor: Uses isOwnerOrStaff to give permissions on a post object.
- IsCommentAuthor: Uses isOwnerOrStaff to give permissions on a comment object.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaff(BasePermission):
    """Allows write access to author and staff.
    Allows read-only access to everyone."""
    owner_field = None

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        owner = getattr(obj, self.owner_field, None)
        return user.is_staff or owner == user


class IsPostAuthor(IsOwnerOrStaff):
    """Allows write access to the post author and staff."""
    owner_field = "author"


class IsCommentAuthor(IsOwnerOrStaff):
    """Allows write access to the comment author and staff."""
    owner_field = "user"
