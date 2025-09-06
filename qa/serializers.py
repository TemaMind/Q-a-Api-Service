"""Сериализаторы DRF для моделей Question и Answer."""

from rest_framework import serializers
from .models import Question, Answer


class QuestionCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания вопроса."""

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionListSerializer(serializers.ModelSerializer):
    """Список вопросов без вложенных ответов."""

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at']


class AnswerSerializer(serializers.ModelSerializer):
    """Базовый сериализатор ответа."""

    class Meta:
        model = Answer
        fields = ['id', 'question', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class AnswerCreateSerializer(serializers.ModelSerializer):
    """Создание ответа без передачи поля question напрямую (берём из URL)."""

    class Meta:
        model = Answer
        fields = ['id', 'user_id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Детальный вопрос с вложенными ответами."""

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'created_at', 'answers']
