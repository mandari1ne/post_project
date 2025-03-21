from django import forms
from .models import Post, Category, PostImage
from django.forms import FileInput


class PostForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['category', 'text', 'file']

        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control'}),
        }
