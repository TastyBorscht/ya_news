import random
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

COMMENT_FORM_DATA = {'text': 'тестовый текст'}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client,
        detail_url
):
    comments_count = Comment.objects.count()
    client.post(detail_url, data=COMMENT_FORM_DATA)
    assert Comment.objects.count() == comments_count


def test_user_can_create_comment(
        author_client,
        detail_url,
        news,
        author
):
    Comment.objects.all().delete()
    response = author_client.post(detail_url, data=COMMENT_FORM_DATA)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {
        'text': f'Какой-то текст, {random.choice(BAD_WORDS)}, еще текст'
    }
    Comment.objects.all().delete()
    response = author_client.post(detail_url, data=bad_words_data)
    assert Comment.objects.count() == 0
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_delete_comment(
        author_client,
        comment,
        detail_url,
        delete_comment_url
):
    response = author_client.delete(delete_comment_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client,
        detail_url,
        comment,
        edit_comment_url,
        news,
        author
):
    response = author_client.post(
        edit_comment_url,
        data=COMMENT_FORM_DATA
    )

    assertRedirects(response, f'{detail_url}#comments')
    comment.refresh_from_db()
    assert comment.text == COMMENT_FORM_DATA['text']
    assert comment.author == author
    assert comment.news == news


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        comment,
        edit_comment_url
):
    old_comment = Comment.objects.get(id=comment.id)
    response = not_author_client.post(
        edit_comment_url,
        data=COMMENT_FORM_DATA
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert old_comment.author == comment.author
    assert old_comment.text == comment.text
    assert old_comment.news == comment.news
