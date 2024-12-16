from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from backend.db import db
from backend.models.trains import Train
from backend.models.stations import Station
from backend.models.schedules import Schedule
from backend.models.dates import Date

trains_bp = Blueprint('trains', __name__)

@trains_bp.route('/trains/search', methods=['GET'])
def search_trains():
    # Получаем параметры запроса и удаляем лишние пробелы
    departure_station_id = request.args.get('departure_station_id', '').strip()
    arrival_station_id = request.args.get('arrival_station_id', '').strip()
    date_str = request.args.get('date', '').strip()

    # Проверка корректности входных параметров
    if not departure_station_id.isdigit() or not arrival_station_id.isdigit() or not date_str:
        return jsonify({"error": "Переданы некорректные данные: departure station ID, arrival station ID, and date."}), 400

    # Преобразуем идентификаторы в целые числа
    departure_station_id = int(departure_station_id)
    arrival_station_id = int(arrival_station_id)

    # Проверка корректности формата даты
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y').date()
    except ValueError:
        return jsonify({"error": "Дата должна быть в формате DD.MM.YYYY."}), 400

    # Получаем все поезда, курсирующие в указанную дату
    valid_dates = Date.query.filter_by(date=date).all()
    train_ids = [date_entry.train_id for date_entry in valid_dates]

    if not train_ids:
        return jsonify({"message": "Поездов на эту дату не было найдено."}), 404

    # Находим все расписания поездов, которые проходят через станцию отправления в указанный день
    departure_schedules = Schedule.query.filter(
        Schedule.train_id.in_(train_ids),
        Schedule.station_id == departure_station_id
    ).all()

    if not departure_schedules:
        return jsonify({"message": "Поезд, следующий через указанные станции в указанный день, НЕ найден."}), 404

    # Фильтруем поезда, которые также проходят через станцию прибытия
    trains = []

    for schedule in departure_schedules:
        arrival_schedule = Schedule.query.filter(
            Schedule.train_id == schedule.train_id,
            Schedule.station_id == arrival_station_id,
            (Schedule.day_in > schedule.day_in) |
            ((Schedule.day_in == schedule.day_in) & (Schedule.arrival_time > schedule.departure_time))
        ).first()

        if arrival_schedule:
            # Рассчитываем дату отправления и прибытия с учетом day_in
            departure_date = date + timedelta(days=schedule.day_in)
            arrival_date = date + timedelta(days=arrival_schedule.day_in)

            # Получаем станции начала и окончания маршрута
            first_schedule = Schedule.query.filter_by(train_id=schedule.train_id).order_by(Schedule.day_in,
                                                                                           Schedule.departure_time).first()
            last_schedule = Schedule.query.filter_by(train_id=schedule.train_id).order_by(Schedule.day_in.desc(),
                                                                                          Schedule.arrival_time.desc()).first()
            start_station = Station.query.get(first_schedule.station_id).name if first_schedule else "Неизвестно"
            end_station = Station.query.get(last_schedule.station_id).name if last_schedule else "Неизвестно"

            train = Train.query.get(schedule.train_id)

            train_info = {
                "train_id": schedule.train_id,
                "train_number": train.number,
                "departure_station": Station.query.get(departure_station_id).name,
                "departure_date": departure_date.strftime('%d.%m.%Y'),
                "departure_time": schedule.departure_time.strftime('%H:%M'),
                "arrival_station": Station.query.get(arrival_station_id).name,
                "arrival_date": arrival_date.strftime('%d.%m.%Y'),
                "arrival_time": arrival_schedule.arrival_time.strftime('%H:%M'),
                "start_station": start_station,  # Станция начала маршрута
                "end_station": end_station,
                "day_in": schedule.day_in
            }
            trains.append(train_info)

    if not trains:
        return jsonify({"message": "Поезд не был найден.."}), 404

    return jsonify(trains)



@trains_bp.route('/trains/train_id=<int:train_id>', methods=['GET'])
def get_train_route(train_id):
    date_str = request.args.get('date', '').strip()

    # Проверка наличия даты
    if not date_str:
        return jsonify({"error": "Дата должна быть в формате DD.MM.YYYY."}), 400

    # Проверка корректности формата даты
    try:
        date = datetime.strptime(date_str, '%d.%m.%Y').date()
    except ValueError:
        return jsonify({"error": "Дата должна быть в формате DD.MM.YYYY."}), 400

    # Проверяем, ездит ли указанный поезд в эту дату
    valid_date = Date.query.filter_by(train_id=train_id, date=date).first()
    if not valid_date:
        return jsonify({"message": "Поездов на указанную дату не найдено."}), 404

    # Получаем все записи расписания для указанного поезда, сортируя по времени отправления
    schedules = Schedule.query.filter_by(train_id=train_id).order_by(Schedule.day_in, Schedule.departure_time).all()

    if not schedules:
        return jsonify({"message": "Поездов с указанными данными не найдено."}), 404

    schedules.sort(key=lambda s: (s.day_in, s.arrival_time or datetime.min.time()))

    # Формируем список всех станций по маршруту
    route = []
    for schedule in schedules:
        # Рассчитываем дату для каждой станции в зависимости от day_in
        station_date = date + timedelta(days=schedule.day_in)

        station_info = {
            "station_name": Station.query.get(schedule.station_id).name,
            "arrival_date": station_date.strftime('%d.%m.%Y') if schedule.arrival_time else None,
            "arrival_time": schedule.arrival_time.strftime('%H:%M') if schedule.arrival_time else None,
            "departure_date": station_date.strftime('%d.%m.%Y') if schedule.departure_time else None,
            "departure_time": schedule.departure_time.strftime('%H:%M') if schedule.departure_time else None
        }
        route.append(station_info)
    train = Train.query.get(train_id)
    return jsonify({
        "train_id": train_id,
        "train_number": train.number,
        "date": date.strftime('%d.%m.%Y'),
        "route": route
    })
