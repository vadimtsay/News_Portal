from django.urls import path
from .views import IndexView

urlpatterns = [
    path('/news/', IndexView.as_view()),
]