from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'reverse_url, parametrized_client, expected_status',
    (
        (
            pytest.lazy_fixture('home_url'),
            pytest.lazy_fixture('unauthorized_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('detail_url'),
            pytest.lazy_fixture('unauthorized_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('users_login_url'),
            pytest.lazy_fixture('unauthorized_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('users_logout_url'),
            pytest.lazy_fixture('unauthorized_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('users_signup_url'),
            pytest.lazy_fixture('unauthorized_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('edit_comment_url'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('edit_comment_url'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('delete_comment_url'),
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK,
        ),
        (
            pytest.lazy_fixture('delete_comment_url'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND,
        ),
    )
)
def test_pages_availability_for_different_users(
        reverse_url,
        parametrized_client,
        expected_status
):
    response = parametrized_client.get(reverse_url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'reversed_url',
    (
        pytest.lazy_fixture('edit_comment_url'),
        pytest.lazy_fixture('delete_comment_url'),
    )
)
def test_redirect_for_anonymous_client(
        client, reversed_url, users_login_url, comment
):
    redirect_url = f'{users_login_url}?next={reversed_url}'
    response = client.get(reversed_url)
    assertRedirects(response, redirect_url)
