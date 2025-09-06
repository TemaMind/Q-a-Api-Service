**Q&A API — Django + DRF + PostgreSQL + Docker**

Небольшой сервис «вопросы–ответы» с REST-эндпоинтами. Реализовано:

1) вопросы (Question): id, text, created_at

2) ответы (Answer): id, question_id, user_id, text, created_at

3) каскадное удаление ответов при удалении вопроса

4) запрет добавления ответа к несуществующему вопросу

5) пользователь может оставить несколько ответов на один вопрос

**Стек**

Django 5 + Django REST Framework (DRF)

PostgreSQL (через psycopg2-binary)

Миграции Django

Docker + docker-compose

Pytest (юнит-тесты без Postgres через SQLite)

**Запуск проекта (Docker)**

1) Раскройте виртуальное окружение 

python m venv venv

venv/Scripts/activate

2) Установите зависимости

pip install -r requirements.txt
pip install -r requirements-dev.txt

3) Подготовьте переменные окружения:

cp .env.example .env


По умолчанию используется: БД qna, пользователь postgres:postgres, хост db (контейнер с Postgres).

Соберите и запустите сервисы:

docker compose up --build


Произойдёт запуск Postgres → ожидание готовности БД → применение миграций → запуск API на http://localhost:8000/.

Полезные команды
# Логи API
docker compose logs -f api

# Выполнить миграции вручную (если нужно)
docker compose exec api python manage.py migrate --noinput

# Остановить и удалить контейнеры
docker compose down

# Полностью сбросить БД (удалить volume)
docker compose down -v

**Эндпоинты**

Вопросы

GET /questions/ — список всех вопросов

POST /questions/ — создать новый вопрос

GET /questions/{id}/ — получить вопрос и все ответы на него

DELETE /questions/{id}/ — удалить вопрос (вместе с ответами)

Ответы

POST /questions/{id}/answers/ — добавить ответ к вопросу

GET /answers/{id}/ — получить конкретный ответ

DELETE /answers/{id}/ — удалить ответ

🧪 Примеры запросов
Bash / Git Bash 
# создать вопрос
curl -X POST http://localhost:8000/questions/ \
  -H 'Content-Type: application/json' \
  -d '{ "text": "Что такое Django?" }'

# список вопросов
curl http://localhost:8000/questions/

# добавить ответ к вопросу 1
curl -X POST http://localhost:8000/questions/1/answers/ \
  -H 'Content-Type: application/json' \
  -d '{ "user_id": "u1", "text": "Веб-фреймворк на Python" }'

# вопрос с ответами
curl http://localhost:8000/questions/1/

# удалить ответ 1
curl -X DELETE http://localhost:8000/answers/1/

# удалить вопрос 1 (удалит и ответы)
curl -X DELETE http://localhost:8000/questions/1/


**Модели (схема)**

1) Question

id: BigAutoField — первичный ключ

text: TextField — текст вопроса

created_at: DateTime(auto_now_add=True) — дата создания

2) Answer

id: BigAutoField

question: ForeignKey(Question, on_delete=models.CASCADE, related_name='answers') — каскадное удаление

user_id: CharField(max_length=64)

text: TextField

created_at: DateTime(auto_now_add=True)

3) Порядок:

вопросы: по убыванию created_at, затем id

ответы: по возрастанию created_at, затем id

**Тесты (pytest)**
Запуск без Postgres (через SQLite)

Удобно для локального быстрого прогона.

pip install -r requirements-dev.txt

$env:DATABASE_URL = 'sqlite:///test.sqlite3'
pytest -q

**Переменные окружения (.env)**
POSTGRES_DB=qna
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_DEBUG=1
DJANGO_SECRET_KEY=dev-secret-key-change-me
ALLOWED_HOSTS=*


Альтернатива: можно задать DATABASE_URL, например postgres://postgres:postgres@localhost:5432/qna. Если есть DATABASE_URL, он имеет приоритет.

##Если возникнут проблемы

Docker не тянет пакетный менеджер apt при сборке
В минимальном Dockerfile шаг с apt-get отсутствует — сборка не должна падать.

relation "qa_question" does not exist / пустая БД
Примените миграции внутри контейнера:

docker compose exec api python manage.py migrate --noinput


Порт 5432 занят
В docker-compose.yml смените маппинг порта у сервиса db:

ports:
  - '5433:5432'
