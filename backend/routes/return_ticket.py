from flask import Blueprint, request, jsonify

from backend.models import Staff, Passenger
from backend.models.tickets import Ticket
from backend.models.users import User
from backend.models.seatsTicket import SeatsTicket
from backend.db import db
import jwt
import os
import logging

from dotenv import load_dotenv
from backend.service.checkToken import get_user_from_token

# Load environment variables from .env file
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')

return_bp = Blueprint('return', __name__)

@return_bp.route('/return', methods=['POST'])
def return_ticket():
    try:
        user_id = get_user_from_token() #вернет 401 если юзер не авторизован

        # Получение данных из запроса
        data = request.get_json()

        required_fields = ['ticket_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Не передан ticket_id."}), 400

        ticket_id = data['ticket_id']

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404

        # Проверка наличия билета
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify({"error": "Билет не найден."}), 404

        # Проверка, принадлежит ли билет указанному пассажиру
        if (not(ticket.buyer_id == user_id or ticket.passenger_id == user_id)):
            return jsonify({"error": "Билет не принадлежит пользователю."}), 403

        # Проверка состояния билета и возможности возврата
        seat_ticket = SeatsTicket.query.filter_by(ticket_id=ticket.id).first()
        if seat_ticket is None:
            return jsonify({"error": "Информация о месте на найдена."}), 404

        if seat_ticket.ticket_state == 'забронирован':
            # Если билет забронирован, удаляем его
            db.session.delete(seat_ticket)
            db.session.delete(ticket)
            db.session.commit()
            return jsonify({"message": "Возврат билета проведен успешно."}), 200

        elif seat_ticket.ticket_state == 'выкуплен':
            # Если билет выкуплен, создаем запрос на возврат
            seat_ticket.ticket_state = 'запрос на возврат'
            db.session.commit()
            return jsonify({"message": "Запрос на возврат оставлен."}), 200
        elif seat_ticket.ticket_state == 'запрос на возврат':
            return jsonify({"error": "Запрос на возврат уже был сформирован."}), 400
        else:
            return jsonify({"error": "Билет не доступен для возврата."}), 400

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке возврата билета.")
        return jsonify({"error": "Internal server error occurred."}), 500


confirm_return_bp = Blueprint('confirm_return', __name__)
@confirm_return_bp.route('/confirm_return', methods=['POST'])
def confirm_return():
    try:
        user_id = get_user_from_token() #вернет 401 если юзер не авторизован

        # Проверка наличия пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "Пользователь не найден."}), 404

        # Проверка, является ли пользователь кассиром
        staff = Staff.query.filter_by(user_id=user_id).first()
        if staff is None:
            return jsonify({"error": "Пользователь не имеет доступа к указному функционалу.."}), 403

        # Получение данных из запроса
        data = request.get_json()

        required_fields = ['ticket_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Не передан ticket_id."}), 400

        ticket_id = data['ticket_id']

        # Проверка наличия билета
        ticket = Ticket.query.get(ticket_id)
        if ticket is None:
            return jsonify({"error": "Билет не найден."}), 404

        # Проверка состояния билета
        seat_ticket = SeatsTicket.query.filter_by(ticket_id=ticket.id).first()
        if seat_ticket is None:
            return jsonify({"error": "Информация о билете не надена."}), 404

        if seat_ticket.ticket_state == 'запрос на возврат' or seat_ticket.ticket_state == 'выкуплен' or \
                seat_ticket.ticket_state == 'забронирован':
            # Удаляем билет и запись о месте
            db.session.delete(seat_ticket)
            db.session.delete(ticket)
            db.session.commit()
            return jsonify({"message": "Билет успешно возвращен."}), 200
        else:
            return jsonify({"error": "Билет не доступен для возврата"}), 400

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при подтверждении возврата билета.")
        return jsonify({"error": "Internal server error occurred."}), 500

@confirm_return_bp.route('/return_requests', methods=['GET'])
def view_return_requests():
    try:
        user_id = get_user_from_token()  # Проверяем авторизацию пользователя

        # Проверяем, является ли пользователь кассиром
        staff = Staff.query.filter_by(user_id=user_id).first()
        if staff is None:
            return jsonify({"error": "Пользователь не имеет доступа к указанному функционалу."}), 403

        # Получаем билеты, которые имеют статус "запрос на возврат"
        return_requests = db.session.query(Ticket, SeatsTicket).join(SeatsTicket, SeatsTicket.ticket_id == Ticket.id).filter(
            SeatsTicket.ticket_state == 'запрос на возврат'
        ).all()

        # Форматируем результат
        tickets_info = []
        for ticket, seat_ticket in return_requests:
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
        logging.exception("Произошла ошибка при получении запросов на возврат билетов.")
        return jsonify({"error": "Internal server error occurred."}), 500