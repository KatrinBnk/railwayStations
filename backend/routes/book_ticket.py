from flask import Blueprint, request, jsonify

from backend.models import Staff
from backend.models.tickets import Ticket
from backend.models.users import User
from backend.models.passengers import Passenger
from backend.models.trains import Train
from backend.models.schedules import Schedule
from backend.models.seats import Seat
from backend.models.dates import Date
from backend.models.comp import Comp
from backend.models.seatsTicket import SeatsTicket
from backend.db import db
from datetime import datetime, timedelta
import jwt
import logging

from dotenv import load_dotenv
import os

from backend.service.checkToken import get_user_from_token
from backend.service.getPassenger import get_passenger_id
# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
SPECIAL_STAFF_CODE = os.getenv('SPECIAL_STAFF_CODE')

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/booking', methods=['POST'])
def book_ticket():
    try:
        user_id = get_user_from_token()

        # Получение данных из запроса
        data = request.get_json()

        required_fields = {'train_id', 'number_wagon', 'seat_number', 'departure_station_id', 'arrival_station_id',
                           'date', 'is_paid', 'passenger_last_name', 'passenger_middle_name',
                           'passenger_first_name', 'passenger_passport'}
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Пожалуйста, укажите все необходимые парамеры: train_id, number_wagon, "
                                     "seat_number, departure_station_id, arrival_station_id, date, is_paid, "
                                     "passenger_last_name, passenger_middle_name,passenger_first_name, "
                                     "passenger_passport"}), 400

        train_id = data['train_id']
        number_wagon = data['number_wagon']
        seat_number = data['seat_number']
        departure_station_id = data['departure_station_id']
        arrival_station_id = data['arrival_station_id']
        date_str = data['date']
        is_paid = data['is_paid']

        # Проверка формата даты
        try:
            travel_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return jsonify({"error": "Дата должна быть в формате DD.MM.YYYY."}), 400

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404
        buyer_id = user_id

        # Проверка наличия поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Поезд не найден."}), 404

        # Проверка наличия расписания поезда на указанную дату
        departure_schedule = Schedule.query.filter_by(train_id=train_id, station_id=departure_station_id).first()
        arrival_schedule = Schedule.query.filter_by(train_id=train_id, station_id=arrival_station_id).first()
        if departure_schedule is None or arrival_schedule is None:
            return jsonify({"error": "Поезд не следует через указанные станции."}), 404

        # Находим вагон по номеру вагона в составе, используя связь через таблицу Date
        date_entry = Date.query.filter_by(train_id=train_id, date=travel_date).first()
        if date_entry is None:
            return jsonify({"error": "Состав поезда на искомую дату не определен."}), 404

        comp = Comp.query.filter_by(id=date_entry.comp_id, number_wagon=number_wagon).first()
        if comp is None:
            return jsonify(
                {"error": "Вагона с таким номером нет в составе поезда."}), 404

        # Проверка наличия вагона и места
        seat = Seat.query.filter_by(wagon_id=comp.wagon_id, number_seat=seat_number).first()
        if seat is None:
            return jsonify({"error": "Заданное место не найдено в вагоне."}), 404

        # Проверка, доступно ли место на указанном маршруте
        existing_seat_tickets = SeatsTicket.query.join(Ticket).filter(
            SeatsTicket.seat_id == seat.id,
            Ticket.train_id == train_id,
            Ticket.date == travel_date
        ).all()

        for seat_ticket in existing_seat_tickets:
            existing_ticket = seat_ticket.ticket
            if not (
                    arrival_schedule.id <= existing_ticket.departure_info or
                    departure_schedule.id >= existing_ticket.arrival_info
            ):
                return jsonify({"error": "Это место уже забронировано."}), 409

        # Расчет времени и цены поездки
        departure_datetime = datetime.combine(travel_date, departure_schedule.departure_time)
        arrival_datetime = datetime.combine(travel_date, arrival_schedule.arrival_time)
        day_difference = arrival_schedule.day_in - departure_schedule.day_in
        arrival_datetime += timedelta(days=day_difference)

        travel_time_minutes = (arrival_datetime - departure_datetime).total_seconds() / 60
        price = travel_time_minutes * 2

        ticket_state = 'выкуплен' if is_paid else 'забронирован'
        cashier_id = None if is_paid else None

        passenger_id = get_passenger_id(
            data['passenger_last_name'],
            data['passenger_first_name'],
            data['passenger_middle_name'],
            data['passenger_passport']
        )

        if passenger_id is None:
            return jsonify({"error": "Ошибка при получении пассажира."}), 500

        # Создание нового билета
        new_ticket = Ticket(
            train_id=train_id,
            date=travel_date,
            arrival_info=arrival_schedule.id,
            departure_info=departure_schedule.id,
            price=price,
            cashier_id=cashier_id,
            passenger_id=passenger_id,
            buyer_id=buyer_id
        )
        db.session.add(new_ticket)
        db.session.flush()

        # Создание записи о бронировании места
        new_seat_ticket = SeatsTicket(
            seat_id=seat.id,
            ticket_id=new_ticket.id,
            ticket_state=ticket_state
        )
        db.session.add(new_seat_ticket)
        db.session.commit()

        return jsonify({"message": "Ticket booked successfully."}), 201

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке бронирования билета.")
        return jsonify({"error": "Internal server error occurred."}), 500


@booking_bp.route('/sell_ticket', methods=['POST'])
def sell_ticket():
    try:
        user_id = get_user_from_token()

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404

        # Проверка, является ли пользователь кассиром
        staff = Staff.query.filter_by(user_id=user_id).first()
        if staff is None:
            return jsonify({"error": "Пользователь не имеет доступа к функционалу кассира."}), 403

        data = request.get_json()

        required_fields = {'train_id', 'number_wagon', 'seat_number', 'departure_station_id', 'arrival_station_id',
                           'date', 'is_paid', 'passenger_last_name', 'passenger_middle_name',
                           'passenger_first_name', 'passenger_passport', 'code_sell'}

        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Пожалуйста, укажите все необходимые парамеры: train_id, number_wagon, "
                                     "seat_number, departure_station_id, arrival_station_id, date, is_paid, "
                                     "passenger_last_name, passenger_middle_name,passenger_first_name, "
                                     "passenger_passport"}), 400

        train_id = data['train_id']
        number_wagon = data['number_wagon']
        seat_number = data['seat_number']
        departure_station_id = data['departure_station_id']
        arrival_station_id = data['arrival_station_id']
        date_str = data['date']
        is_paid = data['is_paid']
        code_sell=data['code-sell']

        if(code_sell != SPECIAL_STAFF_CODE):
            return jsonify({"error": "Указан некорректный код доступа."}), 403
            # Проверка формата даты
        try:
           travel_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            return jsonify({"error": "Дата должна быть в формате DD.MM.YYYY."}), 400

            # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404
        buyer_id = user_id

            # Проверка наличия поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Поезд не найден."}), 404

            # Проверка наличия расписания поезда на указанную дату
        departure_schedule = Schedule.query.filter_by(train_id=train_id, station_id=departure_station_id).first()
        arrival_schedule = Schedule.query.filter_by(train_id=train_id, station_id=arrival_station_id).first()
        if departure_schedule is None or arrival_schedule is None:
            return jsonify({"error": "Поезд не следует через указанные станции."}), 404

            # Находим вагон по номеру вагона в составе, используя связь через таблицу Date
        date_entry = Date.query.filter_by(train_id=train_id, date=travel_date).first()
        if date_entry is None:
            return jsonify({"error": "Состав поезда на искомую дату не определен."}), 404

        comp = Comp.query.filter_by(id=date_entry.comp_id, number_wagon=number_wagon).first()
        if comp is None:
            return jsonify(
                    {"error": "Вагона с таким номером нет в составе поезда."}), 404

            # Проверка наличия вагона и места
        seat = Seat.query.filter_by(wagon_id=comp.wagon_id, number_seat=seat_number).first()
        if seat is None:
            return jsonify({"error": "Заданное место не найдено в вагоне."}), 404

            # Проверка, доступно ли место на указанном маршруте
        existing_seat_tickets = SeatsTicket.query.join(Ticket).filter(
                SeatsTicket.seat_id == seat.id,
                Ticket.train_id == train_id,
                Ticket.date == travel_date
        ).all()

        for seat_ticket in existing_seat_tickets:
            existing_ticket = seat_ticket.ticket
            if not (
                    arrival_schedule.id <= existing_ticket.departure_info or
                    departure_schedule.id >= existing_ticket.arrival_info
            ):
                return jsonify({"error": "Это место уже забронировано."}), 409

            # Расчет времени и цены поездки
        departure_datetime = datetime.combine(travel_date, departure_schedule.departure_time)
        arrival_datetime = datetime.combine(travel_date, arrival_schedule.arrival_time)
        day_difference = arrival_schedule.day_in - departure_schedule.day_in
        arrival_datetime += timedelta(days=day_difference)

        travel_time_minutes = (arrival_datetime - departure_datetime).total_seconds() / 60
        price = travel_time_minutes * 2

        ticket_state = 'выкуплен' if is_paid else 'забронирован'

        passenger_id = get_passenger_id(
                data['passenger_last_name'],
                data['passenger_first_name'],
                data['passenger_middle_name'],
                data['passenger_passport']
        )

        if passenger_id is None:
            return jsonify({"error": "Ошибка при получении пассажира."}), 500

            # Создание нового билета
        new_ticket = Ticket(
                train_id=train_id,
                date=travel_date,
                arrival_info=arrival_schedule.id,
                departure_info=departure_schedule.id,
                price=price,
                cashier_id=buyer_id,
                passenger_id=passenger_id,
                buyer_id=buyer_id
        )
        db.session.add(new_ticket)
        db.session.flush()

            # Создание записи о бронировании места
        new_seat_ticket = SeatsTicket(
                seat_id=seat.id,
                ticket_id=new_ticket.id,
                ticket_state=ticket_state
        )
        db.session.add(new_seat_ticket)
        db.session.commit()

    except Exception as e:
        logging.exception("Произошла непредвиденная ошибка при попытке продажи билета.")
        return jsonify({"error": "Internal server error occurred."}), 500



confirm_booking_bp = Blueprint('confirm_booking', __name__)
@confirm_booking_bp.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    try:
        user_id = get_user_from_token()

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404

        # Проверка, является ли пользователь кассиром
        staff = Staff.query.filter_by(user_id=user_id).first()
        if staff is None:
            return jsonify({"error": "Пользователь не имеет доступа к функционалу кассира."}), 403

        # Получение данных из запроса
        data = request.get_json()
        required_fields = ['ticket_id', 'confirmed']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "В запросе необходимо указать ticket_id и confirmed status (True/False)."}), 400

        ticket_id = data['ticket_id']
        confirmed = data['confirmed']

        # Проверка наличия билета
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify({"error": "Билет не найден."}), 404

        # Проверка состояния билета
        seat_ticket = SeatsTicket.query.filter_by(ticket_id=ticket.id).first()
        if seat_ticket is None:
            return jsonify({"error": "Информация по билету не найдена."}), 404

        if confirmed:
            # Если бронирование подтверждается, необходимо передать цену
            if seat_ticket.ticket_state == 'забронирован':
                # Обновление информации о билете
                if 'price' in data:
                    ticket.price = data['price']
                ticket.cashier_id = staff.user_id

                # Обновление состояния билета на "выкуплен"
                seat_ticket.ticket_state = 'выкуплен'

                db.session.commit()
                return jsonify({"message": "Бронирование успешно подтверждено."}), 200
            else:
                return jsonify({"error": "Указанный билет недоступен для подтверждения бронирования."}), 400
        else:
            print(seat_ticket.ticket_state)
            # Если подтверждение не происходит, билет удаляется
            if seat_ticket.ticket_state == 'забронирован':
                db.session.delete(seat_ticket)
                db.session.delete(ticket)
                db.session.commit()
                return jsonify({"message": "Бронирование успешно снято."}), 200
            elif seat_ticket.ticket_state == 'запрос на возврат':
                seat_ticket.ticket_state = 'забронирован'
                db.session.commit()
            else:
                return jsonify({"error": "Указанный билет не доступен для изменения статуса."}), 400

    except Exception as e:
        return jsonify({"error": "Произошла непредвиденная ошибка при подтверждении бронирования билета."}), 500

@confirm_booking_bp.route('/booking_requests', methods=['GET'])
def view_booking_requests():
    try:
        user_id = get_user_from_token()  # Проверяем авторизацию пользователя

        # Проверяем, является ли пользователь кассиром
        staff = Staff.query.filter_by(user_id=user_id).first()
        if staff is None:
            return jsonify({"error": "Пользователь не имеет доступа к указанному функционалу."}), 403

        # Получаем билеты, которые имеют статус "забронирован"
        booking_requests = db.session.query(Ticket, SeatsTicket).join(SeatsTicket, SeatsTicket.ticket_id == Ticket.id).filter(
            SeatsTicket.ticket_state == 'забронирован'
        ).all()

        # Форматируем результат
        tickets_info = []
        for ticket, seat_ticket in booking_requests:
            passenger = Passenger.query.filter_by(passenger_id=ticket.passenger_id).first()
            buyer = Passenger.query.filter_by(passenger_id=ticket.buyer_id).first()

            if not passenger:
                # Логирование, если информация о покупателе не найдена
                logging.warning(f"Информация о покупателе не найдена для билета {ticket.id}")
                continue

            tickets_info.append({
                "ticket_id": ticket.id,
                "train_number": ticket.train.number,
                "date": ticket.date.strftime('%d.%m.%Y'),
                "buyer_name": f"{buyer.first_name} {buyer.last_name}",
                "passenger_name": f"{passenger.first_name} {passenger.last_name}",
                "passenger_passport": passenger.passport
            })

        return jsonify(tickets_info), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла ошибка при получении запросов на подтверждение бронирования билетов.")
        return jsonify({"error": "Internal server error occurred."}), 500