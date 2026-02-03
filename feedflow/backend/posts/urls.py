"""URL routing for post-related API endpoints."""
from rest_framework.routers import DefaultRouter
from .views import PostViewSet


router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

urlpatterns = router.urls
