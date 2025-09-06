"""Маршруты приложения qa."""

from django.urls import path
from .views import (
    QuestionListCreateView,
    QuestionRetrieveDestroyView,
    AnswerCreateView,
    AnswerRetrieveDestroyView,
)

urlpatterns = [
    path(
        'questions/',
        QuestionListCreateView.as_view(),
        name='question-list-create',
    ),
    path(
        'questions/<int:id>/',
        QuestionRetrieveDestroyView.as_view(),
        name='question-detail-destroy',
    ),
    path(
        'questions/<int:id>/answers/',
        AnswerCreateView.as_view(),
        name='answer-create',
    ),
    path(
        'answers/<int:id>/',
        AnswerRetrieveDestroyView.as_view(),
        name='answer-detail-destroy',
    ),
]
