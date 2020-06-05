from django import forms
from django.contrib.auth.models import User
from .models import MyProfile, Post, PostComment


class UserUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdate(forms.ModelForm):
    bio = forms.CharField(label='Bio', widget=forms.Textarea(attrs={'placeholder': '', 'rows': '5', 'cols': '35'}))

    class Meta:
        model = MyProfile
        fields = ['image', 'birth_date', 'phone_number', 'city', 'state', 'bio']


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'status', 'content']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here!!!', 'rows':'5', 'cols':'45'}))
    class Meta:
        model = PostComment
        fields = ['comment']
