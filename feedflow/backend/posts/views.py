"""
API endpoints for posts.

Includes:
- PostViewSet: API endpoints for posts.
"""
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer
from .permissions import IsPostAuthor, IsCommentAuthor
from .utils import with_post_stats


class PostViewSet(ModelViewSet):
    """Defines API endpoints for posts."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthor]

    def get_queryset(self):
        """Returns the posts query set."""
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


class CommentViewSet(ModelViewSet):
    """Defines API endpoints for comments."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthor]

    def get_queryset(self):
        """Return comments for a specific post."""
        post_id = self.kwargs.get("post_pk")
        return Comment.objects.filter(post_id=post_id).select_related("user")

    def perform_create(self, serializer):
        """Attach authenticated user and post to the comment."""
        serializer.save(
            user=self.request.user,
            post_id=self.kwargs.get("post_pk")
        )
