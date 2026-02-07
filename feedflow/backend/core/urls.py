"""URL configuration for core project."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include("users.auth_urls")),
    path('api/v1/', include("posts.urls")),
    path("api/v1/", include("users.urls"))
]
