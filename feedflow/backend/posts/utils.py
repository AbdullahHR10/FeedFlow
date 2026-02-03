"""
Utilities for post-related querysets.

Includes:
- with_post_stats: Adds reaction and comment statistics to Post querysets.
"""
from django.db.models import Count, Q
from .models import ReactionType


def with_post_stats(queryset):
    """Annotates a Post queryset with reaction and comment counts."""
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
