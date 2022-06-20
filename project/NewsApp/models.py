from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# Create your models here.
class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.authorUser.username}'

    def update_rating(self):
        postrat = self.post_set.aggregate(postRating=Sum('rating'))
        prat = 0
        prat += postrat.get('postRating')

        commentrat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        crat = 0
        crat += commentrat.get('commentRating')

        self.ratingAuthor = prat * 3 + crat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.name}'


class UserCategory(models.Model):
    userThrough = models.ForeignKey(User, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    news = 'NW'
    article = 'AR'
    CATEGORY_CHOICES = (
        (news, 'Новость'),
        (article, 'Статья')
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=article)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}: {self.text}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
