"""URL routing for post-related API endpoints."""
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

posts_router = NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")

urlpatterns = router.urls + posts_router.urls
