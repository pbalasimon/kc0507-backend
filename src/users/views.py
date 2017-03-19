from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import LoginForm


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
            if user is not None:
                django_login(request, user)
                return redirect('home')
            else:
                context["error"] = "Usuario o contraseña no válidos"
        context["form"] = form
        return render(request, 'login.html', context)


def logout(request):
    django_logout(request)
    return redirect('home')
