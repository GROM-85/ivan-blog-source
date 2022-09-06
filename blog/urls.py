from django.urls import path
from .views import StartPage, AllPosts, PostDetails, UnreadPostList,register_page, login_page,logout_page,add_post

urlpatterns = [
    path('register', register_page, name='register'),
    path('login', login_page, name='login'),
    path('logout', logout_page, name='logout'),

    path("", StartPage.as_view(), name='start-page'),
    path('post/', AllPosts.as_view(), name='all-posts'),
    path('post/add', add_post, name='add-post'),
    path("post/to-read", UnreadPostList.as_view(), name="to-read"),
    path('post/<slug:slug>', PostDetails.as_view(), name='post-details'),



]