from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from blogs.forms import PostForm
from blogs.models import Post, Blog


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
    def get(self, request, pk=None):
        form = PostForm()
        post = None
        if pk is not None:
            try:
                post = Post.objects.get(pk=pk)
            except Post.DoesNotExist:
                print("Error al contestar al artículo con pk {0}".format(pk))
                raise Http404
            except Post.MultipleObjectsReturned:
                print("Error al contestar al artículo con pk {0}".format(pk))
                raise Http404

        context = {
            "form": form,
            "post": post
        }
        return render(request, 'blogs/post_new.html', context)

    @method_decorator(login_required)
    def post(self, request, pk=None):
        post = Post(blog=request.user.blog)

        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            if pk is not None:
                post.response = Post.objects.filter(pk=pk).first()
            form.save()
            send_email = self.need_send_email(post)
            if send_email:
                self.send_email_notification(post)
            return redirect(home)
        else:
            message = _("blogs.views.error_create_post")
            context = {
                "post": post,
                "form": form,
                "message": message
            }
            return render(request, 'blogs/post_new.html', context)

    def need_send_email(self, post):
        return post.body.find("@") is not -1 or post.response is not None

    def send_email_notification(self, post):

        username = None
        body = None
        if post.response is None:
            # busco por @username
            inicio_username = post.body.find("@")
            fin_username = post.body.find(" ", inicio_username)
            if fin_username is -1:
                fin_username = len(post.body)
            username = post.body[inicio_username + 1:fin_username]
            body = "Has recibido una mención al artículo '{0}' del usuario '{1}'".format(post.title, username)
        else:
            # busco username al que se contesta el post
            response = Post.objects.filter(pk=post.response.pk).first()
            username = response.blog.user.username
            body = "Has recibido una contestación en el artículo '{0}' del usuario '{1}'".format(post.title,
                                                                                                 username)
        user = User.objects.get(username=username)
        email = user.email
        Post.send_email.delay(email, body)
