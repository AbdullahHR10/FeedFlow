"""
Utilities for post-related querysets.

Includes:
- avatar_upload_path: Defines the path for the user's avatar.
"""
import os
from uuid import uuid4

def avatar_upload_path(instance, filename):
    """Generate a unique upload path for user avatar images."""
    ext = os.path.splitext(filename)[1]
    return f"avatars/users/{instance.user.id}/{uuid4()}{ext}"
