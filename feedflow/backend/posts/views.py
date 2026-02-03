"""
API endpoints for posts.

Includes:
- PostViewSet: API endpoints for posts.
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import IsPostAuthor
from .utils import with_post_stats


class PostViewSet(ModelViewSet):
    """Defines API endpoints for posts."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthor]

    def get_queryset(self):
        """Returns the query set."""
        return (
            with_post_stats(
                Post.objects
                .select_related("author")
                .prefetch_related("media")
            )
        )

    def get_serializer_class(self):
        """Selects the proper seralizer for the action."""
        if self.action in ("create", "update", "partial_update"):
            return PostCreateSerializer

        return PostSerializer

    def perform_update(self, serializer):
        """Sets is_edited to True on update."""
        serializer.save(is_edited=True)
