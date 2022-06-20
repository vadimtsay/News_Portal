from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, Search, PostCreate, PostUpdate, PostDelete, ProfileUpdate, upgrade_me, \
   subscribe_user

#PostUpdate, PostDelete

urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('news/search/', Search.as_view(), name='post_search'),
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('profile/', ProfileUpdate.as_view(), name='profile_update'),
   path('profile/upgrade/', upgrade_me, name='upgrade'),
   path('profile/subscribe/', subscribe_user, name='subscribe'),
]