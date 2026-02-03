from django.contrib import admin
from .models import Post, PostMedia, Reaction, Comment

admin.site.register(Post)
admin.site.register(PostMedia)
admin.site.register(Reaction)
admin.site.register(Comment)
