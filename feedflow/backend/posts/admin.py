from django.contrib import admin
from .models import Post, Reaction, Comment

admin.site.register(Post)
admin.site.register(Reaction)
admin.site.register(Comment)
