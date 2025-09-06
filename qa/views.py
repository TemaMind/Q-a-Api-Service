"""Вьюхи DRF: реализация эндпоинтов по заданию."""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question, Answer
from .serializers import (
    QuestionCreateSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    AnswerSerializer,
    AnswerCreateSerializer,
)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return QuestionCreateSerializer
        return QuestionListSerializer


class QuestionRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'


class AnswerCreateView(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializer

    def create(self, request, *args, **kwargs):
        question_id = kwargs.get('id')
        # Проверяем существование вопроса
        question = get_object_or_404(Question, pk=question_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        answer = Answer.objects.create(
            question=question,
            user_id=serializer.validated_data['user_id'],
            text=serializer.validated_data['text'],
        )
        output = AnswerSerializer(answer)
        headers = self.get_success_headers(output.data)
        return Response(
            output.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AnswerRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Answer.objects.select_related('question').all()
    serializer_class = AnswerSerializer
    lookup_url_kwarg = 'id'
    lookup_field = 'id'
