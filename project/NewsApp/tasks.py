from datetime import timedelta, date

from celery import shared_task
import time

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category
from .signals import weekly_mailing


@shared_task
def weekly_mailing_task():
    print('Еженедельная рассылка')
    weekly_mailing()
