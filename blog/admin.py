from django.contrib import admin
from .models import Post, Tag, Comment


# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'user')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")


admin.site.register(Post, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)


