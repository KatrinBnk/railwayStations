import os

from flask import Blueprint, request, jsonify
import jwt

from backend.db import db
from backend.models import User, Staff, Ticket, SeatsTicket, Passenger
from backend.routes.admin.verification_auth import verification_auth

import logging
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
DELETE_USER_CODE = os.getenv('DELETE_USER_CODE')

delete_user_bp = Blueprint('delete_user', __name__)


@delete_user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    auth_response = verification_auth(DELETE_USER_CODE)
    if auth_response is not None:
        return auth_response

    try:
        # Поиск пользователя
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "User not found."}), 404

            # Удаление билетов, связанных с пользователем
        Ticket.query.filter_by(passenger_id=user_id).delete()
        SeatsTicket.query.filter(SeatsTicket.ticket_id.in_(
            db.session.query(Ticket.id).filter_by(passenger_id=user_id)
        )).delete(synchronize_session=False)

        # Удаление записи из таблицы Staff, если пользователь является сотрудником
        Staff.query.filter_by(user_id=user_id).delete()

        # Удаление записи из таблицы Passenger, если пользователь является пассажиром
        Passenger.query.filter_by(user_id=user_id).delete()

        # Удаление пользователя
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully."}), 200

    except Exception as e:
        logging.exception("Произошла непредвиденная ошибка при удалении пользователя.")
        return jsonify({"error": "Internal server error occurred."}), 500
