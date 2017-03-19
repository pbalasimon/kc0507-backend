from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from blogs.models import Blog, Post
from blogs.permissions import PostPermission
from blogs.serializers import BlogSerializer, BlogPostsSerializer, PostSerializer, PostDetailSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone


class BlogsAPI(ListAPIView):
    queryset = Blog.objects.all().order_by('title')
    serializer_class = BlogSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('user__username',)
    ordering_fields = ('user__username',)


class BlogPostsAPI(ListAPIView):
    serializer_class = BlogPostsSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'summary', 'body',)
    ordering_fields = ('title', 'published_date')

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get('pk', '')
        blog = Blog.objects.get(pk=pk)

        if (user.is_authenticated() and (blog.user_id == user.id)) or user.is_superuser:
            return Post.objects.select_related().filter(blog__id=pk)
        else:
            return Post.objects.select_related().filter(blog__id=pk).filter(published_date__lte=timezone.now())


class PostsAPI(CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)


class PostActionsAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().select_related()
    permission_classes = (PostPermission,)

    def get_serializer_class(self):
        return PostDetailSerializer if self.request.method == 'GET' else PostSerializer
