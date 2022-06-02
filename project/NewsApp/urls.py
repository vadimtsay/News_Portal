from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, Search, PostCreate, PostUpdate, PostDelete
#PostUpdate, PostDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/search/', Search.as_view(), name='post_search'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/create/', PostCreate.as_view(), name='post_create'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]