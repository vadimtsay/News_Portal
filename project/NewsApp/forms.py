from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class CategoryForm(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = {
            'author',
            'postCategory',
            'title',
            'text',
        }
