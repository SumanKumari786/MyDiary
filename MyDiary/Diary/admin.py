from django.contrib import admin
from Diary.models import MyProfile, Post, PostComment, Like


admin.site.register(MyProfile)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(Like)
