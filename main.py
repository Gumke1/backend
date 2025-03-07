import asyncio

from jose import jwt
import Recomendation
import YandexGpt
from authx import AuthXConfig, AuthX
from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.params import Depends
from pydantic import BaseModel, Field
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import request

#from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
#from fastapi import Cookie

app = FastAPI()
origins = [
    "http://localhost:3000",  # Или ваш домен фронтенда
    "http://localhost", #Для запуска без порта
    "*" #НЕ РЕКОМЕНДУЕТСЯ. Только для тестов, разрешает все домены
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']
config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)

#security1 = HTTPBearer()


class UserLoginSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=5, max_length=50)


class SearchingSchema(BaseModel):
    the_search_bar: str


class Tag_Schema(BaseModel):
    tags: str


class Gpt_Schema(BaseModel):
    query: str


class Recommend_Schema(BaseModel):
    user: str


class Favorites_Schema(BaseModel):
    title: str


@app.post('/login')
async def login(creds: UserLoginSchema, response: Response):
    if request.check_nickname(creds.username):
        id = request.input(creds.username, creds.password)
        token = security.create_access_token(uid=str(id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='incorrect username or password')




@app.post('/autorize')
async def autorize(creds: UserLoginSchema, response: Response):
    if request.authorize_us(creds.username, creds.password):
        id = request.get_user_id_by_nickname(creds.username)
        token = security.create_access_token(uid=str(id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {'access_token': token}
    raise HTTPException(status_code=401, detail='incorrect username or password')



def get_user_id(request1: Request):
    # Получение токена из cookies
    token = request1.cookies.get(config.JWT_ACCESS_COOKIE_NAME)

    if not token:
        return {"error": "Token not found in cookies"}

    try:
        # Декодирование токена
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])

        # Извлечение ID пользователя из payload
        user_id = payload.get("sub")  # Обычно идентификатор пользователя хранится в поле "sub"

        if not user_id:
            return {"error": "User ID not found in token"}

        # Преобразуем user_id в число (если он хранится как строка)
        try:
            user_id = int(user_id)  # Преобразуем в целое число
        except (ValueError, TypeError):
            return {"error": "User ID is not a valid number"}

        return user_id  # Возвращаем числовое значение user_id

    except jwt.JWTError as e:
        return {"error": f"Invalid token: {str(e)}"}


@app.post('/favor')
async def login(creds: Favorites_Schema, request1: Request):
    try:
        a = get_user_id(request1)
        request.add_favourites(a, creds.title)
        return {'message': 'ok'}

    except Exception as e:
        return {"error": str(e)}


@app.post('/search_tag')
async def search_tag(creds: SearchingSchema):
    try:
        search = creds.tags
        a = request.search_by_tags(search)
        return a
    except Exception as e:
        return {"error": str(e)}




'''async def access_token_required(my_access_token: str = Cookie(None)):
    if not my_access_token:
        raise HTTPException(status_code=401, detail="Token is missing")

    try:
        payload = jwt.decode(my_access_token, config.JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id'''


@app.get('/recommendations')
async def recommendations(request1: Request):
    try:
        a = get_user_id(request1)
        fav = request.get_favorites(str(a))
        b = Recomendation.system_of_recomend(fav)
        return {"recommendations": b}

    except Exception as e:
        return {"error": str(e)}


@app.get('/all_movies')
async def all_movies():
    res = asyncio.create_task(request.ret_movies())
    movies = await res
    return {'ok': True, 'movies': movies}


@app.get('/action_moves')
async def action_moves():
    res = request.action_tags()
    movies = await res
    return {'ok': True, 'movies': movies}


@app.post('/search_by_gpt')
async def search_by_gpt(creds: Gpt_Schema):
    print(creds)
    try:
        res_gpt = YandexGpt.gpt(creds.query)
        res_bd = request.search_movies(creds.query)
        res_gpt_bd = request.search_movies(*res_gpt)
        print(res_gpt_bd)
        return {'films': res_gpt_bd}
    except Exception as e:
        return {f'error: Invalid query {e}'}


@app.get('/get_favorites')
async def get_favorites(request1: Request):
    try:
        a = get_user_id(request1)
        fav = request.get_favorites(a)
        fav1 = request.favor_movies(fav)
        return {'favorites': fav1}

    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host='127.0.0.1', port=8000)
