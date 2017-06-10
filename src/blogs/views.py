from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from blogs.forms import PostForm
from blogs.models import Post, Blog
from django.utils.translation import gettext as _


def home(request):
    posts = Post.objects.filter().order_by('-published_date')

    context = {
        'posts': posts
    }
    return render(request, 'blogs/home.html', context)


def blogs_list(request):
    blogs = Blog.objects.all()

    context = {
        'blogs': blogs
    }
    return render(request, 'blogs/blogs_list.html', context)


def blog_detail(request, username):
    try:
        user = User.objects.get(username=username)
        blog = Blog.objects.get(user_id=user.pk)
    except Blog.DoesNotExist:
        return render(request, '404.html', {}, status=404)
    except Blog.MultipleObjectsReturned:
        return render(request, '500.html', {}, status=500)

    context = {
        'blog': blog
    }

    return render(request, 'blogs/blog_detail.html', context)


def post_detail(request, username, post_id):
    try:
        user = User.objects.get(username=username)
        post = Post.objects.filter(blog=user.blog.pk, pk=post_id).first()
    except Blog.DoesNotExist:
        return render(request, '404.html', {}, status=404)
    except Blog.MultipleObjectsReturned:
        return render(request, '500.html', {}, status=500)

    context = {
        'post': post
    }

    return render(request, 'blogs/post_detail.html', context)


class NewPostView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = PostForm()

        context = {
            "form": form
        }
        return render(request, 'blogs/post_new.html', context)

    @method_decorator(login_required)
    def post(self, request):
        post = Post(blog=request.user.blog)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save()

            form = PostForm()

            context = {
                "post": post,
                "form": form
            }
            return render(request, 'blogs/post_detail.html', context)
        else:
            message = _("blogs.views.error_create_post")
            context = {
                "post": post,
                "form": form,
                "message": message
            }
            return render(request, 'blogs/post_new.html', context)
