"""URL routing for post-related API endpoints."""
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import PostViewSet, CommentViewSet, ReactionViewSet


router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")

posts_router = NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("comments", CommentViewSet, basename="post-comments")
posts_router.register("reactions", ReactionViewSet, basename="post-reactions")

urlpatterns = router.urls + posts_router.urls
