from django.shortcuts import redirect
from django.utils import translation
from django.views.generic import View


class ChangeLanguage(View):
    def get(self, request, language):
        request.session[translation.LANGUAGE_SESSION_KEY] = language
        return redirect(request.META.get("HTTP_REFERER", "home"))
