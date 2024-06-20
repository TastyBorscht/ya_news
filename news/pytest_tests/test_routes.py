
from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
            ('news:home', None),
            ('news:detail', pytest.lazy_fixture('id_for_news')),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None)
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    response = client.get(reverse(name, args=args))
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_availability_for_comment_edit_and_delete(
        parametrized_client, name, expected_status, id_for_comment
):
    response = parametrized_client.get(reverse(name, args=id_for_comment))
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_redirect_for_anonymous_client(client, name, id_for_comment):
    login_url = reverse('users:login')
    url = reverse(name, args=id_for_comment)
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)