#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Точка входа Django-проекта
import os
import sys


def main():
    # Устанавливаем модуль настроек проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qna.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Не удалось импортировать Django. '
            'Убедитесь, что зависимости установлены.'
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
