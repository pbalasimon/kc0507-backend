from django.urls import reverse

from blogs.models import Blog, Post
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_url(self, blog):
        request = self.context.get("request")
        return request.get_host() + reverse('blog_detail', args=[blog.user])

    def get_username(self, blog):
        return blog.user.username

    class Meta:
        model = Blog
        fields = ("id", "title", "url", "username")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ('blog',)


class PostDetailSerializer(PostSerializer):
    blog = BlogSerializer()


class BlogPostsSerializer(BlogSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'url_image', 'summary', 'published_date', 'posts')
