"""
API endpoints for users.

Includes:
- UserProfileViewSet: API endpoints for users profiles.
"""
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import get_list_or_404
from .serializers import PublicProfileSerializer
from .models import Profile
from .utils import with_profile_stats


class UserProfileViewSet(ReadOnlyModelViewSet):
    """Define API endpoints for users profiles."""
    serializer_class = PublicProfileSerializer
    queryset = Profile.objects.select_related_("user")

    def get_queryset(self):
        """Return the user's profile."""
        return with_profile_stats(
            super().get_queryset(),
            viewer=self.request.user
        )
