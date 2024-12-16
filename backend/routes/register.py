import os

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from backend.models import Staff
from backend.models.users import User
from backend.models.passengers import Passenger
from backend.db import db
import jwt
from datetime import datetime, timedelta
import logging

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')


register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    try:
        # Получение данных из запроса
        data = request.get_json()

        required_fields = ['email', 'password', 'first_name', 'last_name', 'passport']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide email, password, first name, last name, and passport details."}), 400

        email = data['email']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        passport = data['passport']
        middle_name = data.get('middle_name')  # Отчество не является обязательным

        # Проверка, существует ли пользователь с таким email
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists."}), 409

        # Хэширование пароля
        hashed_password = generate_password_hash(password)

        # Создание нового пользователя и пассажира
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()  # Коммит для получения id нового пользователя

        new_passenger = Passenger(
            user_id=new_user.id,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            passport=passport
        )
        db.session.add(new_passenger)
        db.session.commit()

        # Создание токена JWT с действительностью 1 месяц
        payload = {
            "user_id": new_user.id,
            "exp": datetime.utcnow() + timedelta(days=30)  # Токен действителен 1 месяц
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({"message": "Passenger registered successfully.", "token": token}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке регистрации.")
        return jsonify({"error": "Internal server error occurred."}), 500

register_admin_bp = Blueprint('register_admin', __name__)

ADMIN_SECRET_CODE = os.getenv('ADMIN_SECRET_CODE')

@register_admin_bp.route('/register_admin', methods=['POST'])
def register_admin():
    try:
        # Получение данных из запроса
        data = request.get_json()

        # Проверяем обязательные поля
        required_fields = ['email', 'password', 'admin_code', 'first_name', 'last_name', 'station_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: email, password, admin_code, first_name, last_name, station_id."}), 400

        email = data['email']
        password = data['password']
        admin_code = data['admin_code']
        first_name = data['first_name']
        last_name = data['last_name']
        station_id = data['station_id']
        middle_name = data.get('middle_name') if data["middle_name"] else None

        # Проверка специального кода администратора
        if admin_code != ADMIN_SECRET_CODE:
            return jsonify({"error": "Invalid admin code."}), 403

        # Проверка, существует ли уже пользователь с данным email
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists."}), 400

        # Генерация хеша пароля
        hashed_password = generate_password_hash(password)

        # Создание нового пользователя
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.flush()  # Получение ID нового пользователя до коммита

        # Создание нового сотрудника с ролью администратора
        new_staff = Staff(
            user_id=new_user.id,
            station_id=station_id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            position='admin'
        )
        db.session.add(new_staff)
        db.session.commit()

        return jsonify({"message": "Admin registered successfully."}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке регистрации администратора.")
        return jsonify({"error": "Internal server error occurred."}), 500

register_staff_bp = Blueprint('register_staff', __name__)

@register_staff_bp.route('/register_staff', methods=['POST'])
def register_staff():
    try:
        # Получение данных из запроса
        data = request.get_json()

        # Проверка обязательных полей
        required_fields = ['email', 'password', 'admin_code', 'first_name', 'last_name', 'station_id', 'position']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: email, password, admin_code, first_name, last_name, station_id, position."}), 400

        email = data['email']
        password = data['password']
        admin_code = data['admin_code']
        first_name = data['first_name']
        last_name = data['last_name']
        station_id = data['station_id']
        position = data['position']
        middle_name = data.get('middle_name') if data["middle_name"] else None

        # Проверка специального кода администратора
        if admin_code != ADMIN_SECRET_CODE:
            return jsonify({"error": "Invalid admin code."}), 403

        # Проверка, существует ли уже пользователь с данным email
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "User with this email already exists."}), 400

        # Генерация хеша пароля
        hashed_password = generate_password_hash(password)

        # Создание нового пользователя
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.flush()  # Получение ID нового пользователя до коммита

        # Создание нового сотрудника
        new_staff = Staff(
            user_id=new_user.id,
            station_id=station_id,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            position=position
        )
        db.session.add(new_staff)
        db.session.commit()

        return jsonify({"message": "Staff registered successfully."}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке регистрации сотрудника.")
        return jsonify({"error": "Internal server error occurred."}), 500

