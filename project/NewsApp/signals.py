from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.template.loader import render_to_string
from .models import PostCategory, Category, Post


@receiver(m2m_changed, sender=PostCategory)
def mailing_list(sender, instance, *args, **kwargs):
    for cat_id in instance.postCategory.all():
        for user_mailing in cat_id.subscribers.all():
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text[:50],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_mailing.email],
            )
            html_content = render_to_string(
                'subscribe_letter.html',
                {
                    'new': instance,
                    'recipient': user_mailing
                }
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def weekly_mailing():
    if date.today().weekday() == 4:  # если сегодня понедельник
        start = date.today() - timedelta(7)  # вычтем от сегодняшнего дня 7 дней. Это будет началом диапазона выборки
        # дат
        finish = date.today()  # сегодняшний день - конец диапазона выборки дат

        # список постов, отфильтрованный по дате создания в диапазоне start и finish
        list_of_posts = Post.objects.filter(dateCreation__range=(start, finish))

        # все возможные категории
        categories = Category.objects.all()
        print(categories)
        # пробежимся по пользователям
        for user in User.objects.all():
            # создадим список категорий пользователя
            user_categories = []

            user_posts = []
            # возьмём все возможные категории и пробежимся по ним
            for category in categories:
                if category.subscribers.filter(id=user.id).exists():
                    user_categories.append(category.name)
                    for post in list_of_posts:
                        if post.postCategory.filter(id=category.id).exists:
                            user_posts.append(post)

            html_content = render_to_string('weekly_mailing.html',
                                            {'news': user_posts})

            # формируем тело письма
            if len(user_categories):
                msg = EmailMultiAlternatives(
                    subject=f'Все новости за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()  # отсылаем
