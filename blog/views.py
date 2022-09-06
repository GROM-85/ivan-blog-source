import datetime

from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View, TemplateView, DetailView, ListView
from .models import Post, Tag, Comment
from .forms import CommentForm, CustomCreationForm, AddPostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.text import slugify


def register_page(request):
    if request.user.is_authenticated:
        return redirect("start-page")
    else:
        form = CustomCreationForm()

        if request.method == "POST":
            form = CustomCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account was successfully created for " + user)
                return redirect('login')

        context = {
            'form': form,
        }
        return render(request, "blog/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("start-page")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("start-page")
            else:
                messages.info(request, "Username OR Password is incorrect!!!")

        context = {}
        return render(request, "blog/login.html", context)


def logout_page(request):
    logout(request)
    return redirect("login")


def add_post(request):
    post_form = AddPostForm()
    if request.method == "POST":
        post_form = AddPostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            post_form.save_m2m()
            return redirect(to="post-details", slug=post.slug)
    print(post_form.errors.as_data())
    context = {
        "form": post_form,
    }
    return render(request, "blog/add_post.html", context)


@method_decorator(login_required, name="dispatch")
class StartPage(TemplateView):
    template_name = 'blog/start_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # previous_month = timezone.now() - timezone.timedelta(days=30)
        # filtered_post = Post.objects.filter(created__gte=previous_month)[::-1]
        user = self.request.user
        latest_posts = Post.objects.filter(user=user).order_by('-created')
        context['posts'] = latest_posts[:3]
        return context


@method_decorator(login_required, name="dispatch")
class AllPosts(ListView):
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # today = timezone.now().today()
        # return Post.objects.filter(created__range=(today - timezone.timedelta(days=30), today))[::-1]
        user = self.request.user
        return Post.objects.filter(user=user).order_by('-created')


@method_decorator(login_required, name="dispatch")
class PostDetails(View):
    model = Post
    template_name = "blog/post_detail.html"

    def is_stored_post(sefl, request, post_id):
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


@method_decorator(login_required, name="dispatch")
class UnreadPostList(View):
    template_name = 'blog/to_read_posts.html'

    def get(self, request):
        stored_posts = request.session.get("to_read")

        if stored_posts is None or stored_posts == []:
            is_empty = True
            posts = []
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            is_empty = False

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
