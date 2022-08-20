from django.urls import path
from .views import StartPage, AllPosts, PostDetails, UnreadPostList

urlpatterns = [
    path("", StartPage.as_view(), name='start-page'),
    path('post/', AllPosts.as_view(), name='all-posts'),
    path("post/to-read", UnreadPostList.as_view(), name="to-read"),
    path('post/<slug:slug>', PostDetails.as_view(), name='post-details'),
]