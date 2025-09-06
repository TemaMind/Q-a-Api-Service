FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Старт: ждём БД, миграции, gunicorn
CMD bash -lc 'python scripts/wait_for_db.py && \
              python manage.py migrate && \
              gunicorn qna.wsgi:application --bind 0.0.0.0:8000 --workers 2'