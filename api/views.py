from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def get_data(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_data(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
