"""
API endpoints for users.

Includes:
- UserViewSet: API endpoints for users.
- UserProfileViewSet: API endpoints for users public profiles.
"""
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from django.shortcuts import get_list_or_404
from .serializers import UserSerializer, PublicProfileSerializer
from posts.serializers import PostSerializer
from .models import User, Profile
from posts.models import Post
from .utils import with_profile_stats
from posts.utils import with_post_stats


class UserViewSet(ReadOnlyModelViewSet):
    """Define API endpoints for users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        """Return posts written by user."""
        queryset = with_post_stats(
            Post.objects.filter(author_id=pk)
        )

        page = self.paginate_queryset(queryset)
        serializer = PostSerializer(
            page,
            many=True,
            context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class UserProfileViewSet(ReadOnlyModelViewSet):
    """Define API endpoints for users public profiles."""
    serializer_class = PublicProfileSerializer
    queryset = Profile.objects.select_related_("user")

    def get_queryset(self):
        """Return the user's profile."""
        return with_profile_stats(
            super().get_queryset(),
            viewer=self.request.user
        )
