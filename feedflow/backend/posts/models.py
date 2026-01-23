"""Defines the Post, Reaction, Comment classs."""
from django.db import models
from django.conf import settings

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
    content = models.TextField()

    def __str__(self):
        return f"Post #{self.id} by {self.author}"


class ReactionType(models.TextChoices):
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
        unique_together = ("user", "post")

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
