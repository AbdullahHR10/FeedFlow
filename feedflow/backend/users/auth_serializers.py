"""
Serializers for authentication-related endpoints.

Includes:
- SignUpSerializer: Handles user registration, password confirmation,
  user creation, and automatic profile creation.
"""
from rest_framework import serializers
from .models import User, Profile


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for sign up."""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )

        Profile.objects.create(user=user)
        return user
