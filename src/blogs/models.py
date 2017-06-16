from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db import models


class Blog(models.Model):
    class Meta:
        db_table = "Blog"

    user = models.OneToOneField(User, related_name="blog")
    title = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        db_table = "Category"

    name = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        db_table = "Post"

    blog = models.ForeignKey(Blog, related_name="posts")
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    body = models.TextField()
    url_image = models.URLField()
    url_video = models.URLField(null=True, blank=True)
    published_date = models.DateTimeField()
    categories = models.ManyToManyField(Category)
    response = models.ForeignKey('self', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @shared_task
    def send_email(user_email, body):
        email = EmailMessage('Wordplease', body, to=[user_email])
        print("Enviando email '{0}' a '{0}'".format(body, user_email))
        result = email.send()
        print("Email enviado!!!")
