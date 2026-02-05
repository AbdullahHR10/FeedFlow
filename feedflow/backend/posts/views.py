"""
API endpoints for posts.

Includes:
- PostViewSet: API endpoints for posts.
- PostMediaViewSet: API endpoints for post media.
- CommentViewSet: comment on posts.
- ReactionViewSet: create, update, and delete reactions on posts.
"""
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import Follow
from .models import Post, PostMedia, Comment, Reaction
from .serializers import (
    PostSerializer,
    PostMediaSerializer,
    PostCreateSerializer,
    CommentSerializer,
    ReactionSerializer
)
from .permissions import IsPostAuthor, IsCommentAuthor
from .pagination import CursorPagination
from .utils import with_post_stats


class PostViewSet(ModelViewSet):
    """Define API endpoints for posts."""
    permission_classes = [IsAuthenticatedOrReadOnly, IsPostAuthor]
    pagination_class = CursorPagination

    def get_queryset(self):
        """Return the posts query set."""
        return (
            with_post_stats(
                Post.objects
                .select_related("author")
                .prefetch_related("media")
            )
        )

    def get_serializer_class(self):
        """Select the proper seralizer for the action."""
        if self.action in ("create", "update", "partial_update"):
            return PostCreateSerializer

        return PostSerializer

    def perform_update(self, serializer):
        """Set is_edited to True on update."""
        serializer.save(is_edited=True)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="following"
    )
    def following(self, request):
        """Return posts from followed users."""
        followed_ids = Follow.objects.filter(
            follower=request.user
        ).values_list("following_id", flat=True)

        queryset = with_post_stats(
            Post.objects.filter(author_id__in=followed_ids)
        )

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class PostMediaViewSet(ModelViewSet):
    """Define API endpoints for post media."""
    serializer_class = PostMediaSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_queryset(self):
        """Limit media to the selected post."""
        return PostMedia.objects.filter(post_id=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        """Attach media to a post."""
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(post=post)


class CommentViewSet(ModelViewSet):
    """Define API endpoints for comments."""
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


class ReactionViewSet(GenericViewSet):
    """API endpoints for reactions"""
    serializer_class = ReactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Limit reactions to the authenticated user."""
        return Reaction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Handle create/update reaction."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post_id = self.kwargs.get("post_pk")
        post = get_object_or_404(Post, pk=post_id)

        reaction, _ = Reaction.objects.update_or_create(
            user=self.request.user,
            post=post,
            defaults={"type": serializer.validated_data["type"]}
        )

        output_serializer = self.get_serializer(reaction)

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        """Delete the user's reaction from a post."""
        post_id = self.kwargs.get("post_pk")

        reaction = get_object_or_404(
            Reaction,
            user=request.user,
            post_id=post_id
        )

        reaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
