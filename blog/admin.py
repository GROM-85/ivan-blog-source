from django.contrib import admin
from .models import Post, Tag, Author, Comment


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'author')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")


admin.site.register(Post, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Comment, CommentAdmin)


