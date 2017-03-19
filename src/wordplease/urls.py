"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blogs.views import home, blogs_list, blog_detail, post_detail, NewPostView
from users.views import LoginView, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name="home"),
    url(r'^blogs/$', blogs_list, name="blogs_list"),
    url(r'^blogs/(?P<username>[a-zA-Z0-9_]+)/?$', blog_detail, name='blog_detail'),
    url(r'^blogs/(?P<username>[a-zA-Z0-9_]+)/(?P<post_id>[0-9]+)/?$', post_detail, name='post_detail'),
    url(r'^new-post$', NewPostView.as_view(), name="post_new"),
    url(r'^login$', LoginView.as_view(), name="login"),
    url(r'^logout$', logout, name="logout"),
]
