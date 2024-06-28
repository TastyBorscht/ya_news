from datetime import timedelta

import pytest
from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime

from news.models import Comment, News


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Толстой')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель простой')


@pytest.fixture
def unauthorized_client():
    client = Client()
    return client


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        text='Изначальный и трансцендентный Текст коммента',
        author=author,
    )
    return comment


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def edit_comment_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_comment_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


@pytest.fixture
def bulk_of_news():
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=datetime.today() - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def bulk_of_comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
