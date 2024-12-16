import jwt
from flask import request, jsonify
from backend.models.users import User
from backend.models.staffs import Staff
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

def authorize_admin(required_admin_code):
    """
    Проверяет аутентификацию и авторизацию администратора.

    Аргументы:
        required_admin_code (str): Специальный код, который должен быть передан для подтверждения действия.

    Возвращает:
        None, если проверка пройдена успешно, или JSON-ответ с ошибкой, если проверка не пройдена.
    """
    # Извлечение токена из заголовка Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid Authorization header."}), 401

    # Получение токена и его декодирование
    token = auth_header.split(' ')[1]
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token."}), 401

    # Проверка наличия пользователя и его роли администратора
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found."}), 404

    # Проверка, что пользователь является сотрудником с ролью админа
    staff = Staff.query.filter_by(user_id=user_id).first()
    if staff is None or staff.position.lower() != 'admin':
        return jsonify({"error": "User is not authorized to perform this action."}), 403

    # Проверка специального кода администратора, если он передан
    data = request.get_json()
    admin_code = data.get('admin_code')
    if admin_code != required_admin_code:
        return jsonify({"error": "Invalid admin code."}), 403

    # Возвращаем None, если все проверки пройдены успешно
    return None
