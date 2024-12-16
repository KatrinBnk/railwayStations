import os

from dotenv import load_dotenv
from flask import request, jsonify
import jwt
from functools import wraps

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


def get_user_from_token():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        raise ValueError("Неуказан или указан некорректно заголовок авторизации пользователя.")

    token = auth_header.split(' ')[1]
    try:
        # Декодирование токена
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
        if not user_id:
            raise ValueError("Токен не содержит идентификатора пользователя.")
        return user_id
    except jwt.ExpiredSignatureError:
        raise ValueError("Срок действия токена истек.")
    except jwt.InvalidTokenError:
        raise ValueError("Несуществующий токен.")
    except ValueError as e:
        raise e
