from backend.models import Passenger
from backend.db import db
import logging


def get_passenger_id(last_name, first_name, middle_name, passport):
    try:
        # Поиск пассажира по заданным параметрам
        passenger = Passenger.query.filter_by(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            passport=passport
        ).first()

        if passenger:
            return passenger.passenger_id

        # Если пассажир не найден, создаем нового
        new_passenger = Passenger(
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            passport=passport
        )
        db.session.add(new_passenger)
        db.session.commit()

        return new_passenger.passenger_id

    except Exception as e:
        # Обработка ошибок, если произошла ошибка при выполнении запроса или создании пассажира
        db.session.rollback()
        logging.exception("Ошибка при поиске или создании пассажира.")
        return None