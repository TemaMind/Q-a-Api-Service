"""Модели данных: Вопрос и Ответ."""

from django.db import models


class Question(models.Model):
    """Уникальный идентификатор создаётся автоматически (BigAutoField)."""

    text = models.TextField(verbose_name='Текст вопроса')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        """Строковое представление в админке/логах."""
        return f'Question(id={self.id})'


class Answer(models.Model):
    """Связь с вопросом, каскадное удаление."""

    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )
    user_id = models.CharField(max_length=64, verbose_name='ID пользователя')
    text = models.TextField(verbose_name='Текст ответа')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        ordering = ['created_at', 'id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'Answer(id={self.id}, question_id={self.question_id})'
