"""WSGI-конфигурация для gunicorn/uwsgi."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qna.settings')
application = get_wsgi_application()
