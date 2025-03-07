import psycopg2
import json


def input(n, p):

    try:

        data = [n, p]


        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()
        insert_query = """
            INSERT INTO users_table (Nickname, password)
            VALUES (%s, %s);"""

        # Выполнение запроса
        cur.execute(insert_query, data)

        # Фиксация изменений
        conn.commit()

        query = "SELECT id FROM users_table WHERE Nickname = %s"
        cur.execute(query, (n,))
        user_id = cur.fetchone()
        if user_id is None:
            raise "User not found"

        return user_id[0]

        cur.close()
        conn.close()

    except Exception as error:
        print("Ошибка при подключении к PostgreSQL", error)



def get_user_id_by_nickname(nickname):
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(
        user="man",
        password="man",
        host="127.0.0.1",
        port="5432",
        database="my_database"
    )

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # SQL-запрос для получения id пользователя по никнейму
    query = "SELECT id FROM users_table WHERE Nickname = %s;"

    try:
        # Выполняем запрос
        cursor.execute(query, (nickname,))
        result = cursor.fetchone()  # Получаем результат запроса

        if result:
            user_id = result[0]  # Извлекаем id пользователя
            return user_id  # Возвращаем id пользователя
        else:
            return None  # Если пользователь не найден, возвращаем None

    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None

    finally:
        # Закрываем курсор и соединение
        cursor.close()
        conn.close()


def check_nickname(nickname):
    # Устанавливаем соединение с базой данных
    conn = psycopg2.connect(
        user="man",
        password="man",
        host="127.0.0.1",
        port="5432",
        database="my_database"
    )

    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # SQL-запрос для проверки наличия никнейма
    query = "SELECT EXISTS(SELECT 1 FROM users_table WHERE Nickname = %s);"

    # Выполняем запрос
    cursor.execute(query, (nickname,))
    exists = cursor.fetchone()[0]  # Получаем результат запроса

    cursor.close()
    conn.close()

    return not exists  # Возвращаем True, если не найден, иначе False



def add_favourites(user_id, new_favourite):
    conn = psycopg2.connect(
        user="man",
        password="man",
        host="127.0.0.1",
        port="5432",
        database="my_database"
    )

    cursor = conn.cursor()

    # Находим ID пользователя по его имени
    '''find_user_query = """
        SELECT id FROM users_table
        WHERE Nickname = %s;
    """
    cursor.execute(find_user_query, (username,))
    user_id = cursor.fetchone()[0]'''

    # Получаем текущий список избранного
    cursor.execute("SELECT favourites FROM users_table WHERE id = %s;", (user_id,))
    result = cursor.fetchone()

    if result:
        favourites = result[0]

        if favourites:  # Если favourites не пустое
            # Разделяем строку на отдельные фильмы
            favourites_list = [fav.strip() for fav in favourites.split(",")]

            # Проверяем, есть ли новый фильм уже в списке
            if new_favourite.strip() in favourites_list:
                print("Фильм уже добавлен в избранное.")
                cursor.close()
                conn.close()
                return  # Выходим из функции, чтобы не добавлять дубликат

            # Добавляем новый фильм к существующим
            updated_favourites = favourites + ", " + new_favourite
            cursor.execute("UPDATE users_table SET favourites = %s WHERE id = %s;", (updated_favourites, user_id))
            print("Новый фильм добавлен в избранное.")
        else:  # Если favourites пустое
            cursor.execute("UPDATE users_table SET favourites = %s WHERE id = %s;", (new_favourite, user_id))
            print("Новый фильм добавлен, так как избранное было пустым.")
    else:
        print("Пользователь не найден.")

    conn.commit()
    cursor.close()
    conn.close()




'''def search_movies(search_queries):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        all_results = []

        for search_query in search_queries:
            # Шаг 1: Поиск по названию
            title_query = """
                SELECT *
                FROM my_table
                WHERE title ILIKE %s;
            """
            title_pattern = f"%{search_query.lower()}%"
            cur.execute(title_query, (title_pattern,))
            title_results = cur.fetchall()

            if title_results:
                all_results.extend(title_results)
                continue  # Если найдены результаты по названию, переходим к следующему запросу

            # Шаг 2: Поиск по описанию и актёрам (если по названию ничего не найдено)
            description_actor_query = """
                SELECT *
                FROM my_table
                WHERE description ILIKE %s OR actor ILIKE %s;
            """
            description_actor_pattern = f"%{search_query.lower()}%"
            cur.execute(description_actor_query, (description_actor_pattern, description_actor_pattern))
            description_actor_results = cur.fetchall()



            if description_actor_results:
                all_results.extend(description_actor_results)

        return all_results

    except Exception as error:
        print("Ошибка при выполнении запроса:", error)
        return []

    finally:
        # Закрытие соединения с базой данных
        if cur:
            cur.close()
        if conn:
            conn.close()'''




def search_movies(search_queries):
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        all_results = []
        unique_ids = set()  # Для отслеживания уникальных ID фильмов

        for search_query in search_queries:
            # Шаг 1: Поиск по названию
            title_query = """
                SELECT *
                FROM my_table
                WHERE title ILIKE %s;
            """
            title_pattern = f"%{search_query.lower()}%"
            cur.execute(title_query, (title_pattern,))
            title_results = cur.fetchall()

            if title_results:
                for result in title_results:
                    if result[0] not in unique_ids:  # Проверка на уникальность
                        all_results.append(format_result(result))
                        unique_ids.add(result[0])  # Добавляем ID в набор уникальных ID
                continue  # Переходим к следующему запросу

            # Шаг 2: Поиск по описанию и актёрам
            description_actor_query = """
                SELECT *
                FROM my_table
                WHERE description ILIKE %s OR actor ILIKE %s;
            """
            description_actor_pattern = f"%{search_query.lower()}%"
            cur.execute(description_actor_query, (description_actor_pattern, description_actor_pattern))
            description_actor_results = cur.fetchall()

            if description_actor_results:
                for result in description_actor_results:
                    if result[0] not in unique_ids:  # Проверка на уникальность
                        all_results.append(format_result(result))
                        unique_ids.add(result[0])  # Добавляем ID в набор уникальных ID

        return all_results

    except Exception as error:
        print("Ошибка при выполнении запроса:", error)
        return []

    finally:
        # Закрытие соединения с базой данных
        if cur:
            cur.close()
        if conn:
            conn.close()

def format_result(result):
    return {
        "id": result[0],  # Замените индекс в result на соответствующий столбец id
        "title": result[1],  # Замените индекс на соответствующий столбец title
        "tags": result[2],  # Замените индекс на соответствующий столбец tags
        "stars": result[3],  # Замените индекс на соответствующий столбец stars
        "director": result[4],  # Замените индекс на соответствующий столбец director
        "actor": result[5],  # Замените индекс на соответствующий столбец actor
        "year": result[6],  # Замените индекс на соответствующий столбец year
        "runtime": result[7],  # Замените индекс на соответствующий столбец runtime
        "link": result[8],  # Замените индекс на соответствующий столбец link
        "description": result[9]  # Замените индекс на соответствующий столбец description
    }





async def ret_movies():
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
        cur.execute("SELECT * FROM my_table LIMIT 500")  # Замените 'your_table_name' на имя таблицы
        rows = cur.fetchall()

        # Получение названий столбцов
        columns = [column[0] for column in cur.description]

        # Преобразование данных в список словарей
        data = [dict(zip(columns, row)) for row in rows]

        # Преобразование в JSON
        #json_data = json.dumps(data, indent=4)  # indent=4 для красивого форматирования

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




def search_by_tags(search_query):
    try:
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        query = """
            SELECT *
            FROM my_table
            WHERE 
                title ILIKE %s OR
                tags ILIKE %s;   
        """

        search_pattern = f"%{search_query.lower()}%"
        params = (search_pattern, search_pattern)

        cur.execute(query, params)

        rows = cur.fetchall()

        columns = [column[0] for column in cur.description]

        # Преобразование данных в список словарей
        data = [dict(zip(columns, row)) for row in rows]

        return data

    except Exception as error:
        print("Ошибка при выполнении запроса:", error)
        return []

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




async def action_tags():
    try:
        conn = psycopg2.connect(
            user="man",
            password="man",
            host="127.0.0.1",
            port="5432",
            database="my_database"
        )
        cur = conn.cursor()

        query = """
                    SELECT *
                    FROM my_table
                    WHERE tags ILIKE %s;   
                """
        word = 'Action'
        search_pattern = f"%{word.lower()}%"  # Добавляем % для поиска подстроки
        params = (search_pattern,)  # Кортеж с одним элементом

        # Выполнение запроса
        cur.execute(query, params)

        # Получение результатов
        rows = cur.fetchall()

        columns = [column[0] for column in cur.description]

        data = [dict(zip(columns, row)) for row in rows]

        return data

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def get_favorites(user_id):
    conn = psycopg2.connect(
        user="man",
        password="man",
        host="127.0.0.1",
        port="5432",
        database="my_database"
    )

    cursor = conn.cursor()
    find_user_query = """
                    SELECT favourites FROM users_table
                    WHERE id = %s;"""
    cursor.execute(find_user_query, (user_id,))
    fav = cursor.fetchone()
    cursor.close()
    conn.close()

    if fav is None or fav[0] is None:
        return 'Нет избранных фильмов'

    res = fav[0]

    if isinstance(res, str) and ',' in res:
        res1 = res.split(', ')
        return res1
    else:
        return [res] if res is not None else []




def authorize_us(username, password):

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

        # Проверяем, существует ли пользователь с указанным именем и паролем
        query = """
            SELECT id FROM users_table
            WHERE Nickname = %s AND password = %s;
        """
        cur.execute(query, (username, password))
        user_id = cur.fetchone()

        # Если пользователь найден, возвращаем True
        if user_id:
            return True
        else:
            return False

    except Exception as error:
        print("Ошибка при подключении к PostgreSQL:", error)
        return False

    finally:
        # Закрываем соединение
        if cur:
            cur.close()
        if conn:
            conn.close()



def favor_movies(movie_titles: list) -> list:

    data = []
    conn = None
    cur = None

    try:
        # Устанавливаем соединение с базой данных
        conn = psycopg2.connect(
            user="man",  # Замените на ваши учетные данные
            password="man",  # Замените на ваши учетные данные
            host="127.0.0.1",
            port="5432",
            database="my_database"  # Замените на имя вашей базы данных
        )
        cur = conn.cursor()

        # Формируем запрос к базе данных
        #  Предполагаем, что в таблице есть столбец 'title' с названием фильма
        #  Запрос будет искать фильмы, названия которых совпадают с переданными в списке
        placeholders = ', '.join(['%s'] * len(movie_titles))
        query = f"SELECT * FROM my_table WHERE title IN ({placeholders})" # Замените my_table на имя вашей таблицы
        cur.execute(query, movie_titles)
        rows = cur.fetchall()

        # Получение названий столбцов
        columns = [column[0] for column in cur.description]

        # Преобразование данных в список словарей
        data = [dict(zip(columns, row)) for row in rows]

    except psycopg2.Error as error:
        print("Ошибка при подключении к базе данных или выполнении запроса:", error)
        # Обрабатываем специфичные ошибки базы данных
    except Exception as error:
        print("Произошла непредвиденная ошибка:", error)
    finally:
        # Закрываем соединение
        if cur:
            cur.close()
        if conn:
            conn.close()
    return data




