from django.contrib import admin
from django.urls import path
from Diary import views

app_name = 'Diary'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<str:slug>', views.continuepost, name='postcontinue'),
    path('like/', views.like_post, name='like_post')
]
