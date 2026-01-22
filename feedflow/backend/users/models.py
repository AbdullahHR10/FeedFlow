"""Defines the User class."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, F

def avatar_upload_path(instance, filename):
    return f"avatars/users/{instance.user.id}/{filename}"

class User(AbstractUser):
    """Represents a user in the application."""
    pass

class Profile(models.Model):
    """Represents a profile in the application."""
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

class Follow(models.Model):
    """Represents a follow in the application."""
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
