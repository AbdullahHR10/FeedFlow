"""
Utilities for post-related querysets.

Includes:
- media_upload_path: Defines the path for the post's media.
- with_post_stats: Adds reaction and comment statistics to Post querysets.
"""
import os
from django.db.models import Count, Q
from uuid import uuid4


def media_upload_path(instance, filename):
    """Generate a unique upload path for posts media."""
    ext = os.path.splitext(filename)[1]
    return f"media/users/{instance.post.author.id}/{uuid4()}{ext}"


def with_post_stats(queryset):
    """Annotates a Post queryset with reaction and comment counts."""
    from .models import ReactionType
    return queryset.annotate(
        reactions_count=Count("reactions", distinct=True),
        like_count=Count(
            "reactions",
            filter=Q(reactions__type=ReactionType.LIKE),
        ),
        love_count=Count(
            "reactions",
            filter=Q(reactions__type=ReactionType.LOVE),
        ),
        laugh_count=Count(
            "reactions",
            filter=Q(reactions__type=ReactionType.LAUGH),
        ),
        wow_count=Count(
            "reactions",
            filter=Q(reactions__type=ReactionType.WOW),
        ),
        angry_count=Count(
            "reactions",
            filter=Q(reactions__type=ReactionType.ANGRY),
        ),
        comments_count=Count("comments", distinct=True),
    )
