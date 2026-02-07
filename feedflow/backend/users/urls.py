"""URL routing for user-related API endpoints."""
from rest_framework_nested.routers import DefaultRouter
from django.urls import path

from .views import (
    UserViewSet,
    UserProfileViewSet,
    FollowViewSet
)


router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls + [
    path(
        "users/<int:pk>/profile/",
        UserProfileViewSet.as_view({"get": "retrieve"}),
        name="user-profile"
    ),
    path(
        "users/<int:user_pk>/follow/",
        FollowViewSet.as_view({
            "post": "create",
            "delete": "destroy"
        }),
        name="user-follow"
    )
]