import os
from flask import Blueprint, request, jsonify

from backend.models import Schedule
from backend.models.stations import Station
from backend.models.users import User
from backend.models.staffs import Staff
from backend.db import db
from backend.routes.admin.verification_auth import verification_auth
from datetime import datetime
import jwt
import logging

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ADD_STATION_CODE = os.getenv('ADD_STATION_CODE')

stations_bp = Blueprint('stations_bp', __name__, url_prefix='/stations')

@stations_bp.route('/stations/add', methods=['POST'])
def add_station():

    auth_response = verification_auth(ADD_STATION_CODE)
    if auth_response is not None:
        return auth_response

    try:
        # Получение данных из запроса
        data = request.get_json()

        required_fields = ['name', 'city', 'station_id', 'admin_code']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: name, city, admin_code."}), 400

        name = data['name']
        city = data['city']
        station_id = data['station_id']

        # Проверка, существует ли уже станция с таким именем и городом
        if Station.query.filter_by(id=station_id).first():
            return jsonify({"error": "Station with this id already exists."}), 400
        elif Station.query.filter_by(name=name).first():
            return jsonify({"error": "Station with this name already exists."}), 400

        # Создание новой станции
        new_station = Station(id=station_id, name=name, city=city)
        db.session.add(new_station)
        db.session.commit()

        return jsonify({"message": "Station added successfully."}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке добавления новой станции.")
        return jsonify({"error": "Internal server error occurred."}), 500


DELETE_STATION_CODE = os.getenv('DELETE_STATION_CODE')
@stations_bp.route('/stations/delete', methods=['DELETE'])
def delete_station():
    auth_response = verification_auth(DELETE_STATION_CODE)
    if auth_response is not None:
        return auth_response
    try:

        # Получение данных из запроса
        data = request.get_json()

        if not data or 'station_id' not in data or 'admin_code' not in data:
            return jsonify({"error": "Please provide the station_id and admin_code."}), 400

        station_id = data['station_id']

        # Проверка существования станции
        station = Station.query.get(station_id)
        if station is None:
            return jsonify({"error": "Station not found."}), 404

        staffs = Staff.query.filter_by(station_id=station_id).all()
        for staff in staffs:
            user_id = staff.user_id
            db.session.delete(staff)

            user = User.query.get(user_id)
            if user and user.staff is None and user.passenger is None:
                db.session.delete(user)

        schedules = Schedule.query.filter_by(station_id=station_id).all()
        for schedule in schedules:
            db.session.delete(schedule)

        # Удаление станции
        db.session.delete(station)
        db.session.commit()

        return jsonify({"message": "Station deleted successfully."}), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке удаления станции.")
        return jsonify({"error": "Internal server error occurred."}), 500

UPDATE_STATION_CODE = os.getenv('UPDATE_STATION_CODE')

@stations_bp.route('/stations/update', methods=['PUT'])
def update_station():

    auth_response = verification_auth(DELETE_STATION_CODE)
    if auth_response is not None:
        return auth_response

    try:

        # Получение данных из запроса
        data = request.get_json()

        if not data or 'station_id' not in data or 'admin_code' not in data:
            return jsonify({"error": "Please provide the station_id and admin_code."}), 400

        station_id = data['station_id']

        # Проверка существования станции
        station = Station.query.get(station_id)
        if station is None:
            return jsonify({"error": "Station not found."}), 404

        # Обновление информации о станции
        if 'name' in data:
            name = data['name']
            # Проверка уникальности имени станции
            if Station.query.filter(Station.name == name, Station.id != station_id).first():
                return jsonify({"error": "Station with this name already exists."}), 400
            station.name = name

        if 'city' in data:
            city = data['city']
            station.city = city

        if 'new_station_id' in data:
            new_station_id = data['new_station_id']
            # Проверка уникальности нового ID станции
            if Station.query.filter(Station.id == new_station_id).first():
                return jsonify({"error": "Station with this ID already exists."}), 400
            station.id = new_station_id

        db.session.commit()

        return jsonify({"message": "Station updated successfully."}), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке обновления информации о станции.")
        return jsonify({"error": "Internal server error occurred."}), 500
