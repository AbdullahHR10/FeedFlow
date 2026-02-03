"""
Serializers for post-related models.

Includes serializers for:
- PostMedia: media files attached to posts
- Post: public-facing post representation
- PostCreate: post creation and editing
- Reaction: user reactions to posts
- Comment: user comments on posts
"""
from rest_framework import serializers
from .models import PostMedia, Post, Reaction, Comment


class PostMediaSerializer(serializers.ModelSerializer):
    """Serializer for the PostMedia model."""
    class Meta:
        model = PostMedia
        fields = ("id", "file", "type", "order")


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    author = serializers.StringRelatedField(read_only=True)
    media = PostMediaSerializer(many=True, read_only=True)

    reactions = serializers.SerializerMethodField()
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "is_edited",
            "content",
            "created_at",
            "updated_at",
            "media",
            "reactions",
            "comments_count"
        )

    def get_reactions(self, obj):
        return {
            "total": obj.reactions_count,
            "like": obj.like_count,
            "love": obj.love_count,
            "laugh": obj.laugh_count,
            "wow": obj.wow_count,
            "angry": obj.angry_count,
        }


class PostCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating posts."""
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Post
        fields = ("id", "author", "content")

    def validate(self, data):
        """Validates that a post is not empty."""
        if not data.get("content", "").strip():
            raise serializers.ValidationError("Post content cannot be empty.")

        return data

    def update(self, instance, validated_data):
        """Sets is_edited field to be true when the post is updated."""
        new_content = validated_data.get("content", instance.content)

        if new_content != instance.content:
            instance.is_edited = True

        return super().update(instance, validated_data)


class ReactionSerializer(serializers.ModelSerializer):
    """Serializer for the Reaction model."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Reaction
        fields = ("id", "user", "post", "type", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, data):
        """Validate that a user can react only once per post."""
        user = data["user"]
        post = data["post"]

        if Reaction.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You already reacted to this post.")

        return data

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ("id", "user", "post", "content", "created_at")
        read_only_fields = ("created_at",)

    def validate_content(self, value):
        """Validate that a comment is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Comment cannot be empty.")

        return value
