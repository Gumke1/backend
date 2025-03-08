import random

import requests
import time
from random import choice

'''def clean_and_split_movie_list(movie_list):
    combined_string = ' '.join(movie_list)

    # Заменяем переносы строк и лишние пробелы на запятые
    cleaned_string = combined_string.replace('\n', '').replace(' , ', ', ')

    # Разделяем строку по запятым и убираем лишние пробелы вокруг элементов
    split_list = [movie.strip() for movie in cleaned_string.split(',')]

    return split_list'''


def clean_and_split_movie_list(movie_list):
    # Проверка на пустое множество
    if movie_list is None:
        return ['no results']

    # Проверка, является ли movie_list строкой
    if isinstance(movie_list, str):
        if '#' in movie_list:
            return movie_list.split('#')
        elif '/n' in movie_list:
            return movie_list.split('/n')
        elif ', ' in movie_list:
            return movie_list.split(', ')
        return [movie_list]

    # Проверка, является ли movie_list списком
    if isinstance(movie_list, list):
        if '#' in ''.join(movie_list):
            combined_string = ' '.join(movie_list)
            return combined_string.split('#')
        elif '/n' in ''.join(movie_list):
            combined_string = ' '.join(movie_list)
            return combined_string.split('/n')
        elif ', ' in ''.join(movie_list):
            combined_string = ' '.join(movie_list)
            return combined_string.split(', ')
        return movie_list

    # Если тип данных не строка и не список, возвращаем сообщение о типе данных
    return f"Тип данных movie_list: {type(movie_list)}"


def gpt(text):
    a=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    input = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{random.choice(a)} Напиши только строку python, состоящую только из названий фильмов без кавычек с разделителем запятая на английском языке.На тему {text}"
                    }
                ]
            }
        ],

    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer sk-pWEgkG04ngpur3XAKmZ9yQ7GCAqhZ42mXHeB1N3P32kAvf3juydVs55OyecF'
    }

    url_endpoint = "https://api.gen-api.ru/api/v1/networks/gpt-4o-mini"
    response = requests.post(url_endpoint, json=input, headers=headers)

    # Извлекаем request_id из JSON ответа
    try:
        response_json = response.json()
        request_id = response_json.get('request_id')
        print(response_json)  # Выводим json
        if request_id is None:
            print("Ошибка: Не удалось получить 'request_id' из ответа.")
            exit()  # Завершаем выполнение скрипта, если нет request_id
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        exit()

    # Ждем 3 секунды
    time.sleep(5)

    # Формируем URL для второго запроса
    url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'

    # Отправляем второй GET запрос
    response1 = requests.get(url_endpoint1, headers=headers)

    if response1.json().get('result') is None:
        time.sleep(5)
        url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'
        response1 = requests.get(url_endpoint1, headers=headers)
        if response1.json().get('result') is None:
            time.sleep(10)
            url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'
            response1 = requests.get(url_endpoint1, headers=headers)
            print(clean_and_split_movie_list(response1.json().get('result')))
            return clean_and_split_movie_list(response1.json().get('result'))
        response1 = requests.get(url_endpoint1, headers=headers)
        print(clean_and_split_movie_list(response1.json().get('result')))
        return clean_and_split_movie_list(response1.json().get('result'))
    print(clean_and_split_movie_list(response1.json().get('result')))
    return clean_and_split_movie_list(response1.json().get('result'))


