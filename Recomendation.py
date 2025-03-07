import pandas as pd
import Compilation
import psycopg2
import itertools

def system_of_recomend(bests):


    def all_movies():
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

            # Выполняем запрос для получения нужных данных
            cur.execute("""
                SELECT title, tags, stars, actor, director
                FROM my_table
            """)  # Замените 'my_table' на имя вашей таблицы

            # Получаем все строки
            rows = cur.fetchall()

            # Получаем названия столбцов
            columns = [column[0] for column in cur.description]

            # Преобразуем данные в список словарей
            data = [dict(zip(columns, row)) for row in rows]

            # Закрываем соединение с базой данных
            cur.close()
            conn.close()

            # Возвращаем данные
            return data

        except Exception as e:
            # В случае ошибки выводим сообщение и возвращаем пустой список
            print(f"Ошибка при выполнении запроса: {e}")



    # Функция для получения рекомендаций
    def recommend_movies(watched_movie, all_movies):
        recommended = pd.DataFrame(all_movies)

        dfs = [pd.DataFrame(i, index=[0]) for i in watched_movie]

        # Объединяем все DataFrame'ы в один
        result_df = pd.concat(dfs, ignore_index=True)

        sp = []
        for i in range(len(watched_movie)):
            genres = result_df['tags'].values[i]
            print(genres)
            if len(genres.split(', ')) >=2:
                genres = ", ".join(genres.split(', ')[:2])
                print(genres)

            genre_matches = recommended[recommended['tags'].str.contains(genres, na=False)]

            final_recommendations = genre_matches
            list_of_dicts = final_recommendations.to_dict(orient='records')
            titles = [movie['title'] for movie in list_of_dicts]
            titles = set(titles)
            titles = list(titles)
            sp.append(titles)
        flat_list = list(itertools.chain(*sp))
        return flat_list




    # Название просмотренного фильма
    watched_movie_title = bests  # Замените на название вашего фильма


    # Получаем данные о просмотренном фильме
    watched_movie_data = Compilation.for_recom_movies(watched_movie_title)


    all_movies = all_movies()


        # Рекомендуем фильмы
    recommendations = recommend_movies(watched_movie_data, all_movies)


    if recommendations:

        return Compilation.ret_movies(recommendations)
    return 'Ничего не нашлось'

    # Закрываем соединение с базой данных

