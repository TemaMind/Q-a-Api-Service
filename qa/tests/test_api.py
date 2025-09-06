"""Тесты API (pytest + DRF test client)."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from qa.models import Answer


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_create_and_list_questions(client):
    # Создаём вопрос
    r = client.post(
        reverse('question-list-create'),
        data={'text': 'Что такое Django?'},
        format='json',
    )
    assert r.status_code == 201
    qid = r.json()['id']

    # Список вопросов
    r = client.get(reverse('question-list-create'))
    assert r.status_code == 200
    ids = [item['id'] for item in r.json()]
    assert qid in ids


@pytest.mark.django_db
def test_question_detail_with_answers(client):
    # Создаём вопрос
    r = client.post(
        reverse('question-list-create'),
        data={'text': 'Что такое DRF?'},
        format='json'
    )
    qid = r.json()['id']

    # Добавляем два ответа
    answer_url = reverse('answer-create', kwargs={'id': qid})

    r1 = client.post(
        answer_url,
        data={'user_id': 'u1', 'text': 'Django REST Framework'},
        format='json',
    )
    assert r1.status_code == 201

    r2 = client.post(
        answer_url,
        data={'user_id': 'u1', 'text': 'Библиотека для API'},
        format='json',
    )
    assert r2.status_code == 201

    # Получаем вопрос с ответами
    r = client.get(reverse('question-detail-destroy', kwargs={'id': qid}))
    assert r.status_code == 200
    assert len(r.json()['answers']) == 2


@pytest.mark.django_db
def test_get_and_delete_answer(client):
    # Создаём вопрос и ответ
    q_url = reverse('question-list-create')
    r = client.post(q_url, data={'text': 'Удаление ответа?'}, format='json')
    qid = r.json()['id']

    a_url = reverse('answer-create', kwargs={'id': qid})
    a_payload = {'user_id': 'u42', 'text': 'Ответ будет удалён'}
    r = client.post(a_url, data=a_payload, format='json')
    aid = r.json()['id']

    # Получаем ответ
    r = client.get(reverse('answer-detail-destroy', kwargs={'id': aid}))
    assert r.status_code == 200
    assert r.json()['text'] == 'Ответ будет удалён'

    # Удаляем ответ
    r = client.delete(reverse('answer-detail-destroy', kwargs={'id': aid}))
    assert r.status_code == 204


@pytest.mark.django_db
def test_cascade_delete_question(client):
    # Создаём вопрос и два ответа
    r = client.post(
        reverse('question-list-create'),
        data={'text': 'Каскад?'}, format='json'
    )
    qid = r.json()['id']
    client.post(
        reverse('answer-create',kwargs={'id': qid}),
        data={'user_id': 'u1', 'text': 'A1'}, format='json'
    )
    client.post(
        reverse('answer-create', kwargs={'id': qid}),
        data={'user_id': 'u2', 'text': 'A2'}, format='json'
    )

    # Удаляем вопрос
    r = client.delete(reverse('question-detail-destroy', kwargs={'id': qid}))
    assert r.status_code == 204

    # Проверяем, что ответы удалены
    assert Answer.objects.count() == 0
