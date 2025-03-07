import psycopg2
import json
from psycopg2 import sql

def ret_movies(movie_titles):
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        # Формируем SQL-запрос для поиска фильмов по названиям
        query = sql.SQL("""
            SELECT *
            FROM my_table
            WHERE title = ANY(%s)
        """)
        cur.execute(query, (movie_titles,))  # Передаём список названий как параметр

        # Получаем все строки
        rows = cur.fetchall()

        # Получаем названия столбцов
        columns = [column[0] for column in cur.description]

        # Преобразуем данные в список словарей
        data = [dict(zip(columns, row)) for row in rows]

        # Преобразуем в JSON (опционально)
        json_data = json.dumps(data, indent=4)  # indent=4 для красивого форматирования

        return data

    except Exception as error:
        print("Ошибка при выполнении запроса:", error)
        return []

    finally:
        # Закрываем соединение
        if cur:
            cur.close()
        if conn:
            conn.close()


def for_recom_movies(movie_titles):
    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        # Формируем SQL-запрос для поиска фильмов по названиям
        query = sql.SQL("""
            SELECT title, tags, stars, actor, director
            FROM my_table
            WHERE title = ANY(%s)
        """)
        cur.execute(query, (movie_titles,))  # Передаём список названий как параметр

        # Получаем все строки
        rows = cur.fetchall()

        # Получаем названия столбцов
        columns = [column[0] for column in cur.description]

        # Преобразуем данные в список словарей
        data = [dict(zip(columns, row)) for row in rows]

        # Преобразуем в JSON (опционально)
        json_data = json.dumps(data, indent=4)  # indent=4 для красивого форматирования

        return data

    except Exception as error:
        print("Ошибка при выполнении запроса:", error)
        return []


