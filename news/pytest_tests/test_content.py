import pytest
from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('bulk_of_news')
def test_home_page(client, home_url):
    assert (client.get(home_url).context['object_list'].count() == (
            settings.NEWS_COUNT_ON_HOME_PAGE))


def test_news_order(client):
    object_list = client.get(reverse('news:home')).context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.usefixtures('bulk_of_comments', 'news')
def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
