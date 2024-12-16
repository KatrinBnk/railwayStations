from flask import Blueprint, request, jsonify
from backend.models.schedules import Schedule
from backend.models.trains import Train
from backend.models.stations import Station
from backend.db import db
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
ADD_STOP_CODE = os.getenv('ADD_STOP_CODE', 'DEFAULT_ADD_STOP_CODE')

stops_bp = Blueprint('stops_bp', __name__, url_prefix='/stops')

@stops_bp.route('/add', methods=['POST'])
def add_stop():
    #TODO: add auth check

    try:
        # Получение данных из запроса
        data = request.get_json()
        if not data or 'train_id' not in data or 'station_id' not in data or 'arrival_time' not in data or 'departure_time' not in data or 'day_in' not in data:
            return jsonify({"error": "Please provide train_id, station_id, arrival_time, departure_time, and day_in."}), 400

        train_id = data['train_id']
        station_id = data['station_id']
        arrival_time_str = data['arrival_time']
        departure_time_str = data['departure_time']
        day_in = data['day_in']

        # Проверка существования поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Train not found."}), 404

        # Проверка существования станции
        station = Station.query.get(station_id)
        if station is None:
            return jsonify({"error": "Station not found."}), 404

        # Конвертация времени прибытия и отправления
        try:
            arrival_time = datetime.strptime(arrival_time_str, "%H:%M:%S").time()
            departure_time = datetime.strptime(departure_time_str, "%H:%M:%S").time()
        except ValueError:
            return jsonify({"error": "Invalid time format. Expected format: HH:MM:SS."}), 400

        # Проверка валидности параметра day_in
        if not isinstance(day_in, int) or day_in < 0:
            return jsonify({"error": "Invalid day_in. It should be a non-negative integer."}), 400

        # Проверка пересечения остановок
        existing_schedules = Schedule.query.filter_by(train_id=train_id, day_in=day_in).all()
        for schedule in existing_schedules:
            # Проверка, что новая остановка не пересекается по времени с существующими остановками
            if (arrival_time >= schedule.arrival_time and arrival_time <= schedule.departure_time) or \
               (departure_time >= schedule.arrival_time and departure_time <= schedule.departure_time) or \
               (schedule.arrival_time >= arrival_time and schedule.arrival_time <= departure_time):
                return jsonify({
                    "error": f"Time conflict with existing schedule at station {schedule.station_id} on day {day_in}."
                }), 400

        # Создание новой записи остановки в расписании
        new_schedule = Schedule(
            train_id=train_id,
            station_id=station_id,
            arrival_time=arrival_time,
            departure_time=departure_time,
            day_in=day_in
        )

        # Добавление новой остановки в базу данных
        db.session.add(new_schedule)
        db.session.commit()

        return jsonify({"message": "Stop added successfully."}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке добавления остановки в расписание.")
        return jsonify({"error": "Internal server error occurred."}), 500

DELETE_STOP_CODE = os.getenv('DELETE_STOP_CODE', 'DEFAULT_DELETE_STOP_CODE')

@stops_bp.route('/delete', methods=['DELETE'])
def delete_stop():
    #TODO: Проверка авторизации администратора

    try:
        # Получение данных из запроса
        data = request.get_json()
        if not data or 'train_id' not in data or 'station_id' not in data or 'day_in' not in data:
            return jsonify({"error": "Please provide train_id, station_id, and day_in."}), 400

        train_id = data['train_id']
        station_id = data['station_id']
        day_in = data['day_in']

        # Проверка существования поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Train not found."}), 404

        # Проверка существования станции
        station = Station.query.get(station_id)
        if station is None:
            return jsonify({"error": "Station not found."}), 404

        # Проверка валидности параметра day_in
        if not isinstance(day_in, int) or day_in < 0:
            return jsonify({"error": "Invalid day_in. It should be a non-negative integer."}), 400

        # Проверка существования записи остановки в расписании
        schedule_record = Schedule.query.filter_by(train_id=train_id, station_id=station_id, day_in=day_in).first()
        if schedule_record is None:
            return jsonify({"error": "Schedule entry not found for given train_id, station_id, and day_in."}), 404

        # Удаление записи остановки
        db.session.delete(schedule_record)
        db.session.commit()

        return jsonify({"message": "Station stop deleted successfully."}), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке удаления станции из расписания.")
        return jsonify({"error": "Internal server error occurred."}), 500
