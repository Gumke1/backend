import requests
import time


def gpt(text):
    input = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Напиши только название фильма без кавычек на английском языке. {text}"
                    }
                ]
            }
        ]
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
    time.sleep(3)

    # Формируем URL для второго запроса
    url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'

    # Отправляем второй GET запрос
    response1 = requests.get(url_endpoint1, headers=headers)

    if response1.json().get('result') is None:
        time.sleep(2)
        url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'

        # Отправляем второй GET запрос
        response1 = requests.get(url_endpoint1, headers=headers)
        if response1.json().get('result') is None:
            time.sleep(2)
            url_endpoint1 = f'https://api.gen-api.ru/api/v1/request/get/{request_id}'

            # Отправляем второй GET запрос
            response1 = requests.get(url_endpoint1, headers=headers)
            return response1.json().get('result')
        return response1.json().get('result')
    return response1.json().get('result')
