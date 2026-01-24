"""Defines User, Profile and Follow serializers."""
from rest_framework import serializers
from .models import User, Profile, Follow


class UserSerializer(serializers.ModelSerializer):
    """User class serializer."""
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    """Profile class serializer."""
    user = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Profile
        fields = ("id", "user", "bio", "avatar")


class FollowSerializer(serializers.ModelSerializer):
    """Follow class serializer."""
    follower = serializers.HiddenField(
        default = serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = ("follower", "following", "created_at")
        read_only_fields = ("created_at",)

