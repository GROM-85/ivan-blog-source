from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_data, name="api_get_data"),
    path("add/", views.add_data, name="api_post_data")
]