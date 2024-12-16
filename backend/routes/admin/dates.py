import os
from flask import Blueprint, request, jsonify

from backend.models import Ticket, SeatsTicket, Comp, Wagon
from backend.models.dates import Date
from backend.models.trains import Train
from backend.db import db
from backend.routes.admin.verification_auth import verification_auth
import logging
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ADD_DATE_CODE = os.getenv('ADD_DATE_CODE', 'DEFAULT_ADD_CODE')

dates_bp = Blueprint('dates_bp', __name__, url_prefix='/dates')

@dates_bp.route('/dates/add', methods=['POST'])
def add_date():
    auth_response = verification_auth(ADD_DATE_CODE)
    if auth_response is not None:
        return auth_response

    try:
        # Получение данных из запроса
        data = request.get_json()

        # Проверка наличия необходимых полей в запросе
        required_fields = ['train_id', 'date', 'admin_code']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: train_id, date, and admin_code."}), 400

        train_id = data['train_id']
        train_date_str = data['date']
        comp_id = data.get('comp_id')
        new_composition = data.get('new_composition')

        # Преобразование даты из строки в datetime.date
        try:
            train_date = datetime.strptime(train_date_str, '%d.%m.%Y').date()
        except ValueError:
            return jsonify({"error": "Date format should be DD.MM.YYYY."}), 400

        # Проверка существования поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Train not found."}), 404

        # Проверка на использование существующего состава
        if comp_id:
            existing_comps = Comp.query.filter_by(id=comp_id).all()
            if not existing_comps:
                return jsonify({"error": "Composition with the specified ID not found."}), 404

            # Добавление записи о дате с существующим составом
            new_date = Date(date=train_date, train_id=train_id, comp_id=comp_id)
            db.session.add(new_date)
            db.session.commit()

            return jsonify({"message": "Date added successfully with existing composition."}), 201

        # Проверка на создание нового состава
        elif new_composition:
            if 'comp_id' not in new_composition or 'wagons' not in new_composition:
                return jsonify({"error": "Please provide 'comp_id' and 'wagons' in new composition."}), 400

            new_comp_id = new_composition['comp_id']
            wagons = new_composition['wagons']

            # Проверка, что состав с указанным comp_id не существует
            existing_comps = Comp.query.filter_by(id=new_comp_id).first()
            if existing_comps:
                return jsonify({"error": "Composition with the specified ID already exists."}), 400

            # Создание нового состава с вагонами
            for wagon in wagons:
                if 'wagon_id' not in wagon or 'number_wagon' not in wagon or 'type_id' not in wagon:
                    return jsonify({"error": "Each wagon entry must include 'wagon_id', 'number_wagon', and 'type_id'."}), 400

                wagon_id = wagon['wagon_id']
                number_wagon = wagon['number_wagon']
                type_id = wagon['type_id']

                # Проверка существования вагона, если его нет - создаем
                existing_wagon = Wagon.query.filter_by(id=wagon_id).first()
                if not existing_wagon:
                    new_wagon = Wagon(id=wagon_id, type=type_id)
                    db.session.add(new_wagon)

                # Создание записи состава (Comp)
                new_comp = Comp(id=new_comp_id, wagon_id=wagon_id, number_wagon=number_wagon)
                db.session.add(new_comp)

            # Создание записи о дате с новым составом
            new_date = Date(date=train_date, train_id=train_id, comp_id=new_comp_id)
            db.session.add(new_date)

            # Сохранение всех изменений в базе данных
            db.session.commit()

            return jsonify({"message": "Date and new composition added successfully."}), 201

        # Если не передан ни существующий comp_id, ни new_composition
        return jsonify({"error": "Please provide either an existing 'comp_id' or 'new_composition'."}), 400

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при добавлении даты следования поезда.")
        return jsonify({"error": "Internal server error occurred."}), 500



DELETE_DATE_CODE = os.getenv('DELETE_DATE_CODE', 'DEFAULT_DELETE_CODE')


@dates_bp.route('/dates/delete', methods=['DELETE'])
def delete_date():
    auth_response = verification_auth(DELETE_DATE_CODE)
    if auth_response is not None:
        return auth_response

    try:
        # Получение данных из запроса
        data = request.get_json()
        if not data or 'train_id' not in data or 'admin_code' not in data or 'dates' not in data:
            return jsonify({"error": "Please provide train_id, admin_code, and dates list."}), 400

        train_id = data['train_id']
        admin_code = data['admin_code']
        dates = data['dates']  # Ожидается, что это список строк в формате "YYYY-MM-DD"

        # Проверка существования поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Train not found."}), 404

        # Удаление каждой указанной даты для данного поезда
        for date_str in dates:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": f"Invalid date format for '{date_str}'. Expected format: YYYY-MM-DD."}), 400

            # Поиск даты в базе данных для указанного поезда
            date_record = Date.query.filter_by(date=date_obj, train_id=train_id).first()
            if date_record is None:
                return jsonify({"error": f"Date '{date_str}' not found for this train."}), 404

            # Поиск всех билетов, связанных с этой датой и поездом
            tickets = Ticket.query.filter_by(train_id=train_id, date=date_obj).all()
            if tickets:
                for ticket in tickets:
                    # Удаление всех связанных с билетом записей из таблицы seatsTickets
                    seats_tickets = SeatsTicket.query.filter_by(ticket_id=ticket.id).all()
                    for seat_ticket in seats_tickets:
                        db.session.delete(seat_ticket)

                    # Удаление самого билета
                    db.session.delete(ticket)

            # Удаление записи даты из сессии
            db.session.delete(date_record)

        # Сохранение изменений в базе данных
        db.session.commit()

        return jsonify({"message": "Dates and related tickets deleted successfully."}), 200

    except Exception as e:
        # Логирование ошибки и возврат ответа с 500 статусом
        logging.exception("Произошла непредвиденная ошибка при попытке удаления дат следования для поезда.")
        return jsonify({"error": "Internal server error occurred."}), 500
