import os

from flask import Blueprint, request, jsonify

from backend.db import db
from backend.models import Train, Comp, Date, Wagon, Ticket, SeatsTicket, Schedule
from .verification_auth import verification_auth

import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
CREATE_TRAIN_CODE = os.getenv('CREATE_TRAIN_CODE')

train_bp = Blueprint('train_bp', __name__, url_prefix='/trains')


@train_bp.route('/trains/add', methods=['POST'])
def create_train():
    auth_response = verification_auth(CREATE_TRAIN_CODE)
    if auth_response is not None:
        return auth_response
    try:

        data = request.get_json()

        required_fields = ['train_id', 'number', 'type', 'date', 'admin_code']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: train_id, number, type."}), 400

        train_id = data['train_id']
        number = data['number']
        train_type = data['type']
        train_date_str = data['date']
        comp_id = data.get('comp_id')
        new_composition = data.get('new_composition')

        # Преобразование даты из строки в datetime.date
        try:
            train_date = datetime.strptime(train_date_str, '%d.%m.%Y').date()
        except ValueError:
            return jsonify({"error": "Date format should be DD.MM.YYYY."}), 400

        # Создание нового поезда
        new_train = Train(id=train_id, number=number, type=train_type)
        db.session.add(new_train)

        if comp_id:
            existing_comps = Comp.query.filter_by(id=comp_id).all()
            if not existing_comps:
                return jsonify({"error": "Composition with the specified ID not found."}), 404

            for comp in existing_comps:
                new_date = Date(date=train_date, train_id=train_id, comp_id=comp.id)
                db.session.add(new_date)
                db.session.commit()
                return jsonify({"message": "Train and composition created successfully."}), 201

        elif new_composition:

            if 'comp_id' not in new_composition or 'wagons' not in new_composition:
                return jsonify({"error": "Please provide 'comp_id' and 'wagons' in new composition."}), 400

            new_comp_id = new_composition['comp_id']
            wagons = new_composition['wagons']

            existing_comps = Comp.query.filter_by(id=comp_id).all()
            if existing_comps:
                return jsonify({"error": "Composition with the specified ID found."}), 404

            for wagon in wagons:
                wagon_id = wagon['wagon_id']
                number_wagon = wagon['number_wagon']

                existing_wagon = Wagon.query.filter_by(id=wagon_id).all()
                if not existing_wagon:
                    type_id = wagon['type_id']
                    new_wagon = Wagon(id=wagon_id, type=type_id)
                    db.session.add(new_wagon)
                    db.session.commit()

                new_comp = Comp(id=new_comp_id, wagon_id=wagon_id, number_wagon=number_wagon)
                db.session.add(new_comp)

            new_date = Date(date=train_date, train_id=train_id, comp_id=new_comp_id)
            db.session.add(new_date)

            db.session.commit()

            return jsonify({"message": "Train and composition created successfully."}), 201

    except Exception as e:
        logging.exception("Произошла непредвиденная ошибка при создании поезда.")
        return jsonify({"error": "Internal server error occurred."}), 500


DELETE_TRAIN_CODE = os.getenv('DELETE_TRAIN_CODE')


@train_bp.route('/trains/delete/<int:train_id>', methods=['DELETE'])
def delete_train(train_id):
    auth_response = verification_auth(DELETE_TRAIN_CODE)
    if auth_response is not None:
        return auth_response

    try:
        data = request.get_json()

        required_fields = ['admin_code']
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Please provide all required fields: train_id, number, type."}), 400

        # Поиск поезда
        train = Train.query.get(train_id)
        if train is None:
            return jsonify({"error": "Train not found."}), 404
        # Удаление билетов, связанных с поездом
        Ticket.query.filter_by(train_id=train_id).delete()
        # Удаление записей о местах, связанных с билетами
        SeatsTicket.query.filter(SeatsTicket.ticket_id.in_(
            db.session.query(Ticket.id).filter_by(train_id=train_id)
        )).delete(synchronize_session=False)
        # Удаление расписания, связанного с поездом
        Schedule.query.filter_by(train_id=train_id).delete()
        # Удаление дат, связанных с поездом
        Date.query.filter_by(train_id=train_id).delete()
        # Удаление поезда
        db.session.delete(train)

        db.session.commit()

        return jsonify({"message": "Train and related schedules deleted successfully."}), 200

    except Exception as e:
        logging.exception("Произошла непредвиденная ошибка при удалении поезда.")
        return jsonify({"error": "Internal server error occurred."}), 500
