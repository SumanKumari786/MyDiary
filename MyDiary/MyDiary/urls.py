"""MyDiary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import Diary
from Diary import views
from Diary.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.fun, name="click here"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('changepass/', views.changePass, name='changepass'),
    path('view/', views.view_status, name='view'),
    path('private/', views.private, name='private'),
    path('Diary/', include('Diary.urls', namespace='Diary')),

    # Update profile Views
    path('view_profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    # POST views
    path('view_status/', PostListView.as_view(), name='view_status'),
    path('view_status/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('view_status/<int:pk>/update', PostUpdateView.as_view(), name='post_update'),
    path('view_status/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),


    # password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='Diary/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='Diary/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='Diary/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='Diary/password_reset_complete.html'),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
