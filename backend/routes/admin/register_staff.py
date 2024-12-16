from flask import Blueprint, request, jsonify
from backend.models.users import User
from backend.models.staffs import Staff
from backend.models.stations import Station
from backend.db import db
import logging
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from backend.routes.admin.verification_auth import verification_auth

# Загрузка переменных окружения
load_dotenv()
REGISTER_STAFF_CODE = os.getenv('REGISTER_STAFF_CODE', 'DEFAULT_REGISTER_CODE')

register_staff_bp = Blueprint('register_staff_bp', __name__)

@register_staff_bp.route('ф', methods=['POST'])
def register_staff():
    auth_response = verification_auth(REGISTER_STAFF_CODE)
    if auth_response is not None:
        return auth_response

    try:
        # Получение данных из запроса
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data or 'first_name' not in data or 'last_name' not in data or 'position' not in data or 'station_id' not in data:
            return jsonify({"error": "Please provide email, password, first_name, last_name, position, and station_id."}), 400

        email = data['email']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        middle_name = data.get('middle_name')  # Опционально
        position = data['position']
        station_id = data['station_id']

        # Проверка существования станции
        station = Station.query.get(station_id)
        if station is None:
            return jsonify({"error": "Station not found."}), 404

        # Проверка уникальности email
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists."}), 400

        # Создание нового пользователя
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.flush()

        # Создание записи в таблице Staff
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
