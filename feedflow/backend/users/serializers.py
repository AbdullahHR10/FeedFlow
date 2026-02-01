"""
Serializers for user-related models.

Includes serializers for:
- User: public-facing user information
- Profile: user profile data linked to the authenticated user
- Follow: follower–following relationships between users
"""
from rest_framework import serializers
from .models import User, Profile, Follow


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "avatar")


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    follower = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ("follower", "following", "created_at")
        read_only_fields = ("created_at",)


    def validate_following(self, following):
        """Validate that a user cannot follow themselves or
        follow the same user twice."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return following

        follower = request.user

        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself.")

        if Follow.objects.filter(
            follower=follower,
            following=following
        ).exists():
            raise serializers.ValidationError("You already follow this user.")

        return following
