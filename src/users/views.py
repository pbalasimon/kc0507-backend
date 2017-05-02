from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from blogs.models import Blog
from users.forms import LoginForm, SignupForm


class LoginView(View):
    def get(self, request):
        context = {
            'form': LoginForm()
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        context = dict()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None and hasattr(user, 'blog'):
                django_login(request, user)
                return redirect('home')
            else:
                context["error"] = "Usuario o contraseña no válidos"
        context["form"] = form
        return render(request, 'login.html', context)


class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html', {
            'form': SignupForm()
        })

    def post(self, request):
        form = SignupForm(request.POST)
        context = dict()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            new_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            blog_created = Blog.objects.create(
                user=new_user,
                title='El blog de ' + new_user.username,
                created_date=timezone.now()
            )
            if new_user and blog_created:
                django_login(request, new_user)
                return redirect('home')
            else:
                context['error'] = "Error creando usuario"

        context['form'] = form
        return render(request, 'signup.html', context)


def logout(request):
    django_logout(request)
    return redirect('home')
