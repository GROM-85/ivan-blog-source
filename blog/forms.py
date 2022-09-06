from django import forms
from .models import Comment, Post, Tag
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name": "Name",
            "email": "E-mail",
            "text": "Text",
            "post": "Post",
        }
        error_messages = {
            "user_name": {
                "required": "Username shouldn't be empty!",
                "max_length": "The Max length is 120 char!",
            },
            "email": {
                "required": "Email shouldn't be empty!",
            },
            "text": {
                "required": "Text shouldn't be empty!",
                "max_length": "The Max length is 300 char!"
            }
        }


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["slug", "updated", "created", "user"]

    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )