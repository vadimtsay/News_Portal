from django import forms
from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post, Category, Author


class PostFilter(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gt',
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'categoryType': ['exact'],
        }
