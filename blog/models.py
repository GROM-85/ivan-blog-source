from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'


class Tag(models.Model):
    caption = models.TextField()

    def __str__(self):
        return self.caption


class Post(models.Model):

    title = models.CharField(max_length=50)
    content = models.TextField(validators=[MinLengthValidator(limit_value=10,
                                                              message='The minimum length of the'
                                                                      ' text should be at least 10 char ')])
    excerpt = models.CharField(max_length=150, blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="images", null=True)
    updated = models.DateTimeField("Updated", auto_now=True)
    created = models.DateTimeField('Created')
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='posts', blank=True, null=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f"Title: {self.title}; Created: {self.created}; Author: {self.author}"


class Comment(models.Model):
    user_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    text = models.TextField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True )

    def str(self):
        return f"{self.user_name}, {self.post}, {self.email}"
