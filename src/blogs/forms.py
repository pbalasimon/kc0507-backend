from django import forms
from django.utils.translation import gettext_lazy as _

from blogs.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "summary", "body", "url_image", "url_video", "published_date", "categories"]

        widgets = {
            'title': forms.TextInput(
                attrs={'id': 'title', 'class': 'form-control', 'placeholder': _("blogs.forms.title.placeholder")}),
            'summary': forms.TextInput(
                attrs={'id': 'summary', 'class': 'form-control', 'placeholder': _("blogs.forms.summary.placeholder")}),
            'body': forms.Textarea(attrs={'id': 'body', 'class': 'form-control'}),
            'url_image': forms.URLInput(
                attrs={'id': 'url_image', 'class': 'form-control',
                       'placeholder': _("blogs.forms.url_image.placeholder")}),
            'url_video': forms.URLInput(attrs={'id': 'url_video', 'class': 'form-control',
                                               'placeholder': _("blogs.forms.url_video.placeholder")}),
            'published_date': forms.DateInput(
                attrs={'id': 'published_date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'categories': forms.SelectMultiple(attrs={'id': 'categories', 'class': 'form-control'})
        }
        error_messages = {
            'title': {
                'required': _("blogs.forms.title.required")
            },
            'summary': {
                'required': _("blogs.forms.summary.required")
            },
            'body': {
                'required': _("blogs.forms.body.required")
            },
            'url_image': {
                'required': _("blogs.forms.url_image.required")
            },
            'published_date': {
                'required': _("blogs.forms.published_date.required")
            },
        }
