from flask import Blueprint, request, jsonify
from backend.db import db
from backend.models import Train, Schedule, Seat, Comp, Date, Ticket, SeatsTicket, Wagon, TypeWagon
from datetime import datetime, timedelta

seats_bp = Blueprint('seats', __name__)

@seats_bp.route('/seats', methods=['GET'])
def get_seats_trains():
    try:
        # Извлечение параметров из запроса
        train_id = request.args.get('train_id', type=int)
        departure_station_id = request.args.get('departure_station_id', type=int)
        arrival_station_id = request.args.get('arrival_station_id', type=int)
        date = request.args.get('date').strip()

        # Проверка и парсинг даты
        try:
            parsed_date = datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            return jsonify({"error": "Неверный формат даты. Используйте формат дд.мм.гггг"}), 400

        # Получение comp_id из таблицы dates
        date_entry = Date.query.filter_by(train_id=train_id, date=parsed_date.date()).first()
        if not date_entry:
            return jsonify({"error": "Состав для данного поезда и даты не найден"}), 404
        comp_id = date_entry.comp_id

        # Получение вагонов для состава
        wagons = Comp.query.filter_by(id=comp_id).all()
        wagon_ids = [wagon.wagon_id for wagon in wagons]
        wagon_number_map = {wagon.wagon_id: wagon.number_wagon for wagon in wagons}  # Сопоставление wagon_id и номера вагона

        # Получение всех мест для этих вагонов
        all_seats = Seat.query.join(Wagon, Seat.wagon_id == Wagon.id).join(
            TypeWagon, Wagon.type == TypeWagon.id
        ).filter(
            Seat.wagon_id.in_(wagon_ids)  # Фильтруем места только по текущим вагонам
        ).all()

        # Фильтрация только доступных мест
        available_seats = []
        for seat in all_seats:
            # Проверяем, если запись в SeatsTicket существует
            existing_seat_tickets = SeatsTicket.query.join(Ticket).filter(
                SeatsTicket.seat_id == seat.id,
                Ticket.train_id == train_id,
                Ticket.date == parsed_date.date()
            ).all()

            # Если записи не существует, добавляем место в список доступных
            if not existing_seat_tickets:
                available_seats.append(seat)

        # Логика рассчета времени в пути
        schedules = Schedule.query.filter(
            Schedule.train_id == train_id,
            Schedule.station_id.in_([departure_station_id, arrival_station_id])
        ).order_by(Schedule.day_in).all()

        if len(schedules) != 2:
            return jsonify({"error": "Неверные станции или поезд не проходит через указанные станции"}), 404

        departure_schedule, arrival_schedule = schedules
        if departure_schedule.day_in > arrival_schedule.day_in or (
            departure_schedule.day_in == arrival_schedule.day_in and
            departure_schedule.departure_time >= arrival_schedule.arrival_time
        ):
            return jsonify({"error": "Станция отправления должна быть раньше станции прибытия"}), 400

        departure_datetime = datetime.combine(parsed_date.date(), departure_schedule.departure_time)
        arrival_datetime = datetime.combine(
            parsed_date.date() + timedelta(days=(arrival_schedule.day_in - departure_schedule.day_in)),
            arrival_schedule.arrival_time
        )
        travel_time_minutes = int((arrival_datetime - departure_datetime).total_seconds() // 60)

        # Формирование цены
        price = travel_time_minutes * 2

        # Формирование ответа
        seats_data = [{
            "wagon_number": wagon_number_map[seat.wagon_id],
            "number_seat": seat.number_seat,
            "type_wagon": seat.wagon.type_wagon.description,
            "type_seat": seat.type_seat
        } for seat in available_seats]

        return jsonify({
            "available_seats": seats_data,
            "price": price,
            "travel_time_minutes": travel_time_minutes
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

