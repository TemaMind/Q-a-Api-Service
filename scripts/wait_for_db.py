"""Скрипт ожидания готовности Postgres в Docker."""

import os
import sys
import time

import psycopg2
import dj_database_url


def get_conn_params():
    url = os.getenv('DATABASE_URL')
    if url:
        cfg = dj_database_url.parse(url)
        return {
            'dbname': cfg['NAME'],
            'user': cfg['USER'],
            'password': cfg['PASSWORD'],
            'host': cfg['HOST'],
            'port': cfg['PORT'] or 5432,
        }
    return {
        'dbname': os.getenv('POSTGRES_DB', 'qna'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'host': os.getenv('POSTGRES_HOST', 'db'),
        'port': int(os.getenv('POSTGRES_PORT', '5432')),
    }


def wait():
    params = get_conn_params()
    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(**params)
            conn.close()
            print('Database is ready')
            return
        except Exception as e:
            if time.time() - start > 60:
                print(f'Timed out waiting for database: {e}', file=sys.stderr)
                sys.exit(1)
            time.sleep(1)


if __name__ == '__main__':
    wait()
