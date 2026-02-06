"""
Utilities for user-related querysets.

Includes:
- avatar_upload_path: Defines the path for the user's avatar.
- with_profile_stats: Adds follower, following, post counts, and follow state
"""
import os
from uuid import uuid4
from django.db.models import Count, Exists, OuterRef, Value


def avatar_upload_path(instance, filename):
    """Generate a unique upload path for user avatar images."""
    ext = os.path.splitext(filename)[1]
    return f"avatars/users/{instance.user.id}/{uuid4()}{ext}"


def with_profile_stats(queryset, viewer=None):
    """Annotates a Profile queryset with user stats."""
    from .models import Follow
    qs = queryset.annotate(
        follower_count=Count("user__followers", distinct=True),
        following_count=Count("user__following", distinct=True),
        posts_count=Count("user__posts", distinct=True)
    )

    if viewer and viewer.is_authenticated:
        qs = qs.annotate(
            is_following=Exists(
                Follow.objects.filter(
                    follower=viewer,
                    following=OuterRef("user_id")
                )
            )
        )
    else:
        qs = qs.annotate(is_following=Value(False))

    return qs
