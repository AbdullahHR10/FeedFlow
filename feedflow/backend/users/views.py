"""
API endpoints for users.

Includes:
- UserViewSet: API endpoints for users.
- UserProfileViewSet: API endpoints for users public profiles.
- FollowViewSet: API endpoints for follow.
"""
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserSerializer,
    PublicProfileSerializer,
    FollowSerializer
)
from posts.serializers import PostSerializer
from .models import User, Profile, Follow
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
    queryset = Profile.objects.select_related("user")

    def get_queryset(self):
        """Return public profiles with viewer-related stats."""
        return with_profile_stats(
            super().get_queryset(),
            viewer=self.request.user
        )


class FollowViewSet(GenericViewSet):
    """Define API endpoints for follow."""
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        """Create a follow between users."""
        serializer = self.get_serializer(
            data={"following": kwargs["user_pk"]},
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """Delete a follow between users."""
        Follow.objects.filter(
            follower=request.user,
            following_id=kwargs["user_pk"]
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
