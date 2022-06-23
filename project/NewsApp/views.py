from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm, ProfileForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect


class NewsList(ListView):
    model = Post
    ordering = 'dateCreation',
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_news'] = len(Post.objects.all())
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_single.html'
    context_object_name = 'news_single'


class Search(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# Добавляем новое представление для создания заметки.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('NewsApp.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        current_url = self.request.path
        post = form.save(commit=False)
        post.author = Author.objects.get(authorUser=self.request.user.id)
        if current_url.split('/')[1] == 'news':
            post.categoryType = self.model.news
        else:
            post.categoryType = self.model.article
        return super(PostCreate, self).form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsApp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_update.html'
    success_url = '/'


# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsApp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not Author.objects.filter(id=user.id).exists():
        Author.objects.create(authorUser=user)
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/profile')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'profile_update.html'
    success_url = '/'

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not user.groups.filter(name='authors').exists()
        context['category'] = Category.objects.all()
        user_cat = list()
        for u in Category.objects.all():
            if u.subscribers.filter(id=user.id).exists():
                user_cat.append(u.name)
        context['user_category'] = user_cat
        return context


def subscribe_user(request):
    user = request.user
    print(user)
    category = Category.objects.get(id=request.POST['id_cat'])
    print(category)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    else:
        category.subscribers.add(user)
    return redirect('/profile')
