from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
import datetime


class Tag(models.Model):
    caption = models.TextField()

    def __str__(self):
        return self.caption


def get_upload_path(instance, filename):
    return f"user_{instance.user.username}/{filename}"


class Post(models.Model):

    title = models.CharField(max_length=50)
    content = models.TextField(validators=[MinLengthValidator(limit_value=5,
                                                              message='The minimum length of the'
                                                                      ' text should be at least 5 char ')])
    excerpt = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=get_upload_path, null=True)
    updated = models.DateTimeField("Updated", auto_now=True)
    created = models.DateTimeField('Created')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.created = datetime.datetime.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Title: {self.title}; Created: {self.created}; Author: {self.user}"


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True )

    def str(self):
        return f"{self.user_name}, {self.post}, {self.email}"
