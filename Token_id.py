from fastapi import FastAPI, Response
from authx import AuthX, AuthXConfig
from datetime import datetime, timedelta

app = FastAPI()

# Настройка конфигурации AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_REFRESH_COOKIE_NAME = 'my_refresh_token'
config.JWT_TOKEN_LOCATION = ['cookies']
config.JWT_COOKIE_CSRF_PROTECT = False

auth = AuthX(config)

@app.post("/logout")
async def logout(response: Response):
    # Удаляем access token cookie
    response.delete_cookie(key=config.JWT_ACCESS_COOKIE_NAME)

    # Удаляем refresh token cookie (если используется)
    response.delete_cookie(key=config.JWT_REFRESH_COOKIE_NAME)

    return {"message": "Successfully logged out"}

# Альтернативный способ: установка cookie с истекшим сроком действия
@app.post("/logout-alt")
async def logout_alt(response: Response):
    # Устанавливаем access token cookie с истекшим сроком действия
    response.set_cookie(
        key=config.JWT_ACCESS_COOKIE_NAME,
        value="",  # Пустое значение
        max_age=0,  # Срок действия истек
        expires=0,  # Срок действия истек
        httponly=True,
        secure=True,  # Используйте True, если используете HTTPS
        samesite="lax",
    )

    # Устанавливаем refresh token cookie с истекшим сроком действия (если используется)
    response.set_cookie(
        key=config.JWT_REFRESH_COOKIE_NAME,
        value="",  # Пустое значение
        max_age=0,  # Срок действия истек
        expires=0,  # Срок действия истек
        httponly=True,
        secure=True,  # Используйте True, если используете HTTPS
        samesite="lax",
    )

    return {"message": "Successfully logged out"}