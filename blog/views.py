from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View, TemplateView, DetailView, ListView
from .models import Post, Author, Tag, Comment
from .forms import CommentForm


class StartPage(TemplateView):
    template_name = 'blog/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # previous_month = timezone.now() - timezone.timedelta(days=30)
        # filtered_post = Post.objects.filter(created__gte=previous_month)[::-1]
        latest_posts = Post.objects.order_by('-created')
        context['posts'] = latest_posts[:3]
        return context


class AllPosts(ListView):
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        today = timezone.now().today()
        # return Post.objects.filter(created__range=(today - timezone.timedelta(days=30), today))[::-1]
        return Post.objects.order_by('-created')


class PostDetails(View):
    model = Post
    template_name = "blog/post_detail.html"

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("to_read")
        if stored_posts is not None:
            is_set_to_read = post_id in stored_posts
        else:
            is_set_to_read = False
        return is_set_to_read

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comment_form = CommentForm()
        post_comments = post.comments.order_by("-pk")[:3]
        context = {}
        context['post'] = post
        context['tags'] = post.tag.all()
        context['comment_form'] = comment_form
        context['comment_list'] = post_comments
        context['is_set_to_read'] = self.is_stored_post(request, post.id)
        return render(request, self.template_name, context)

    ''' IF YOU USE <input type="hidden" name="slug" value="{{post.slug}}"> and call POST within the same View,
     so you have to add slug key-word arg. to def post(self,request,slug)'''

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(to="post-details", slug=slug)

        context = {
            "post": post,
            "tags": post.tag.all(),
            "comment_form": comment_form,
            "comment_list": post.comments.order_by("-pk")[:3],
            "is_set_to_read": self.is_stored_post(request, post.id)

        }
        return render(request, self.template_name, context)


class UnreadPostList(View):
    template_name = 'blog/to_read_posts.html'

    def get(self, request):
        stored_posts = request.session.get("to_read")
        posts = Post.objects.filter(id__in=stored_posts)

        if not stored_posts:
            is_empty = False
        else:
            is_empty = True

        context = {
            "post_to_read": posts,
            "is_empty": is_empty,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        post_id = int(request.POST["post_id"])
        slug = Post.objects.get(id=post_id).slug
        # we call get(), instead request.session[""], cause is key doesnt exists, we got KeyValueError
        # first time get() --> returns None
        stored_posts = request.session.get("to_read")

        if stored_posts is None:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["to_read"] = stored_posts

        return redirect(to="post-details", slug=slug)
