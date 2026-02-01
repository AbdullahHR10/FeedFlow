"""
Database models for user-related tables.

Includes:
- User: custom user model extending Django's AbstractUser
- Profile: one-to-one user profile with additional metadata
- Follow: follower–following relationship between users
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F
from uuid import uuid4
import os


def avatar_upload_path(instance, filename):
    """Generate a unique upload path for user avatar images."""
    ext = os.path.splitext(filename)[1]
    return f"avatars/users/{instance.user.id}/{uuid4()}{ext}"


class User(AbstractUser):
    """
    Represents a user in the application.

    Extends from Django's AbstractUser.
    """
    pass


class Profile(models.Model):
    """
    Represents a profile for the user.

    Stores user-specific metadata that does not belong on the core User model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True
    )

    def __str__(self):
        """Return a string representation of the profile."""
        return f"Profile of {self.user.username}"


class Follow(models.Model):
    """
    Represents a follow relationship between two users.

    Enforces uniqueness and prevents self-following.
    """
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow"
            ),
            models.CheckConstraint(
                condition=~Q(follower=F("following")),
                name="prevent_self_follow"
            )
        ]
        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"])
        ]

    def __str__(self):
        """Return a string representation of the follow."""
        return f"{self.follower} → {self.following}"
