from flask import Blueprint, request, jsonify

from backend.models import Staff
from backend.models.tickets import Ticket
from backend.models.users import User
from backend.models.passengers import Passenger
from backend.models.schedules import Schedule
from backend.db import db
import jwt
import os
import logging
from sqlalchemy import or_

from dotenv import load_dotenv
from backend.service.checkToken import get_user_from_token

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

view_tickets_bp = Blueprint('view_tickets', __name__)


@view_tickets_bp.route('/tickets', methods=['GET'])
def view_tickets():
    try:
        user_id = get_user_from_token() #вернет 401 если юзер не авторизован

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found."}), 404

        tickets = Ticket.query.filter(or_(
                Ticket.buyer_id == user_id,
                Ticket.passenger_id == user_id
            )).all()

        # Форматирование информации о билетах для вывода
        tickets_info = []
        for ticket in tickets:
            role = "buyer and passenger" if ticket.buyer_id == user_id and ticket.passenger_id == user_id else (
                "buyer" if ticket.buyer_id == user_id else "passenger"
            )
            print(ticket.arrival_schedule.departure_time)

            tickets_info.append({
                "ticket_id": ticket.id,
                "train_number": ticket.train.number,
                "date": ticket.date.strftime('%d.%m.%Y'),
                "departure_station_id": ticket.departure_info,
                "departure_station_name": ticket.departure_schedule.station.name,
                "departure_time": ticket.departure_schedule.arrival_time.strftime('%H:%M'),
                "arrival_station_id": ticket.arrival_info,
                "arrival_station_name": ticket.arrival_schedule.station.name,
                "arrival_time": ticket.arrival_schedule.arrival_time.strftime('%H:%M'),
                "price": ticket.price,
                "status": next((st.ticket_state for st in ticket.seat_ticket), "нет информации"),
                "role": role
            })
        print(tickets_info)
        return jsonify(tickets_info), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при просмотре билетов.")
        return jsonify({"error": "Internal server error occurred."}), 500


ticket_details_bp = Blueprint('ticket_details', __name__)


@ticket_details_bp.route('/ticket/<int:ticket_id>', methods=['GET'])
def view_ticket(ticket_id):
    try:
        user_id = get_user_from_token() #вернет 401 если юзер не авторизован

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404

        # Проверка, является ли пользователь кассиром или пассажиром
        is_cashier = Staff.query.filter_by(user_id=user_id).first() is not None
        is_passenger = Passenger.query.filter_by(user_id=user_id).first() is not None

        if not is_cashier and not is_passenger:
            return jsonify({"error": "Пользователь не имеет доступа к просмотру."}), 403

        # Проверка наличия билета
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify({"error": "Билет не найден."}), 404

        # Проверка, если пользователь — пассажир, то билет должен принадлежать ему
        if is_passenger and (ticket.passenger_id != user_id or ticket.buyer_id != user_id):
            return jsonify({"error": "Пользователь не имеет доступа к просмотру."}), 403

        # Формирование полной информации о билете
        ticket_info = {
            "ticket_id": ticket.id,
            "train_id": ticket.train_id,
            "train_number": ticket.train.number if ticket.train else "Unknown",
            "date": ticket.date.strftime('%d.%m.%Y'),
            "departure_station_id": ticket.departure_info,
            "departure_station_name": ticket.departure_schedule.station.name if ticket.departure_schedule else "Unknown",
            "departure_time": ticket.departure_schedule.departure_time.strftime(
                '%H:%M') if ticket.departure_schedule else "Unknown",
            "arrival_station_id": ticket.arrival_info,
            "arrival_station_name": ticket.arrival_schedule.station.name if ticket.arrival_schedule else "Unknown",
            "arrival_time": ticket.arrival_schedule.arrival_time.strftime(
                '%H:%M') if ticket.arrival_schedule else "Unknown",
            "price": ticket.price,
            "passenger_id": ticket.passenger_id,
            "passenger_name": f"{ticket.passenger.first_name} {ticket.passenger.last_name}" if ticket.passenger else "Unknown",
            "cashier_id": ticket.cashier_id,
            "cashier_name": f"{ticket.cashier.first_name} {ticket.cashier.last_name}" if ticket.cashier else "Unknown",
            "status": next((st.ticket_state for st in ticket.seat_ticket), "нет информации")
        }

        return jsonify(ticket_info), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при просмотре билета.")
        return jsonify({"error": "Internal server error occurred."}), 500
