from django.contrib import admin
from .models import Post, PostComment, Tag, Image, Video, Like, Reply


admin.site.register((Post, Tag, Image, Video, Like, PostComment,Reply,))
