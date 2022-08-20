from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = "__all__"
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