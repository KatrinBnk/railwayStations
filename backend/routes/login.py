import os

import jwt
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from backend.models import Passenger, Staff
from backend.models.users import User

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Настраиваем логирование для отладки
logging.basicConfig(level=logging.DEBUG)

SECRET_KEY = os.getenv('JWT_SECRET_KEY')
login_bp = Blueprint('login', __name__)


@login_bp.route('/login', methods=['POST'])
def login():
    try:
        # Получение данных из запроса
        data = request.get_json()

        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Please provide email and password."}), 400

        email = data['email']
        password = data['password']

        # Поиск пользователя по email
        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"error": "User with this email is not registered in the system."}), 404

        # Проверка хэшированного пароля
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password."}), 401

        # Создание токена JWT с действительностью 1 месяц
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(days=30)  # Токен действителен 1 месяц
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        passenger = Passenger.query.filter_by(user_id=user.id).first()
        staff = Staff.query.filter_by(user_id=user.id).first()
        if staff:
            return jsonify({"token": token, "role": "staff"})
        elif passenger:
            return jsonify({"token": token, "role": "passenger"})
        else:
            return jsonify({"error":"User not found!"}), 404

    except Exception as e:
        return jsonify({"error": "Internal server error occurred."}), 500
