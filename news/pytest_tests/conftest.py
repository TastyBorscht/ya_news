from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews import settings


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
def id_for_news(news):
    return (news.id,)


@pytest.fixture
def id_for_comment(comment):
    return (comment.id,)


@pytest.fixture
def bulk_of_news():
    all_news = [
        News(title=f'Новость {index}', text='Просто текст.')
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


@pytest.fixture
def detail_url(id_for_news):
    return reverse('news:detail', args=id_for_news)


@pytest.fixture
def comment_form_data():
    return {'text': 'тестовый текст'}
