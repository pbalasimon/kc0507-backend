from django import forms

from blogs.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "summary", "body", "url_image", "url_video", "published_date", "categories"]

        widgets = {
            'title': forms.TextInput(attrs={'id': 'title', 'class': 'form-control', 'placeholder': 'Título'}),
            'summary': forms.TextInput(attrs={'id': 'summary', 'class': 'form-control', 'placeholder': 'Introducción'}),
            'body': forms.Textarea(attrs={'id': 'body', 'class': 'form-control'}),
            'url_image': forms.URLInput(
                attrs={'id': 'url_image', 'class': 'form-control', 'placeholder': 'URL Imagen'}),
            'url_video': forms.URLInput(attrs={'id': 'url_video', 'class': 'form-control', 'placeholder': 'URL Video'}),
            'published_date': forms.DateInput(
                attrs={'id': 'published_date', 'class': 'form-control', 'placeholder': 'dd/mm/aaaa'}),
            'categories': forms.SelectMultiple(attrs={'id': 'categories', 'class': 'form-control'})
        }
        error_messages = {
            'title': {
                'required': 'El título es obligatorio'
            },
            'summary': {
                'required': 'La introducción es obligatoria'
            },
            'body': {
                'required': 'El texto es obligatorio'
            },
            'url_image': {
                'required': 'La url de la imagen es obligatoria'
            },
            'published_date': {
                'required': 'La fecha y hora de publicación es obligatoria'
            },
        }
