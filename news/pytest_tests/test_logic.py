from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(
        client,
        comment_form_data,
        detail_url
):
    client.post(detail_url, data=comment_form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client,
        detail_url,
        comment_form_data,
        news,
        author
):
    response = author_client.post(detail_url, data=comment_form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


#     COMMENT_TEXT = 'Текст комментария'
#     NEW_COMMENT_TEXT = 'Обновлённый комментарий'


def test_author_can_delete_comment(
        author_client,
        id_for_comment,
        detail_url
):
    response = author_client.delete(
        reverse('news:delete', args=id_for_comment)
    )
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(
        author_client,
        id_for_comment,
        comment_form_data,
        detail_url,
        comment
):
    response = author_client.post(
        reverse('news:edit', args=id_for_comment),
        data=comment_form_data
    )

    assertRedirects(response, f'{detail_url}#comments')
    comment.refresh_from_db()
    assert comment.text == comment_form_data['text']


def test_user_cant_edit_comment_of_another_user(
        not_author_client,
        id_for_comment,
        comment_form_data,
        comment
):
    response = not_author_client.post(
        reverse('news:edit', args=id_for_comment),
        data=comment_form_data
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    old_text = comment.text
    comment.refresh_from_db()
    assert old_text == comment.text
