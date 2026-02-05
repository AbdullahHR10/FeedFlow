"""
Database models for post-related tables.

Includes:
- Post: user-generated posts
- PostMedia: media files attached to posts
- Reaction: reactions to posts
- Comment: user comments on posts
"""
from django.db import models
from django.conf import settings
from .utils import media_upload_path

User = settings.AUTH_USER_MODEL


class PostBaseModel(models.Model):
    """Defines common attributes for other classes."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Post(PostBaseModel):
    """Represents a post in the application."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    is_edited = models.BooleanField(default=False)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"Post #{self.id} by {self.author}"


class MediaType(models.TextChoices):
    """Defines allowed values for media fields."""
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"


class PostMedia(PostBaseModel):
    """Represents media attached to a post."""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="media"
    )
    file = models.FileField(upload_to=media_upload_path)
    type = models.CharField(
        max_length=10,
        choices=MediaType.choices
    )
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "created_at"]

class ReactionType(models.TextChoices):
    """Defines allowed values for reaction fields"""
    LIKE = "like", "Like"
    LOVE = "love", "Love"
    LAUGH = "laugh", "Haha"
    WOW = "wow", "Wow"
    ANGRY = "angry", "Angry"


class Reaction(PostBaseModel):
    """Represents a reaction in the application."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    type = models.CharField(
        max_length=10,
        choices=ReactionType.choices,
        default=ReactionType.LIKE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_reaction"
            )
        ]

    def __str__(self):
        return f"{self.user} - reaction on post #{self.post_id}"


class Comment(PostBaseModel):
    """Represents a comment in the application."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.TextField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user} - comment on post #{self.post_id}"
