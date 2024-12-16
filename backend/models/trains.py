from sqlalchemy.orm import relationship

from backend.db import db
from sqlalchemy import Enum

import re

def validate_train_number(number):
    pattern = r'^[0-9]{3}[А-Яа-я]?$'
    if not re.match(pattern, number):
        raise ValueError("Неверный формат номера поезда")

class Train(db.Model):
    __tablename__ = 'trains'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(4), unique=True, nullable=False)
    type = db.Column(Enum('скоростной', 'скорый', 'высокоскоростной', 'пассажирский', name='train_type'), nullable=False)

    dates = relationship("Date", back_populates="train")
    schedules = relationship("Schedule", back_populates="train")
    tickets = relationship("Ticket", back_populates="train")

    __table_args__ = (
        db.CheckConstraint(
            "number ~ '^[0-9]{3}[А-Яа-я]$'",
            name='check_number_format'
        ),
    )

    def __init__(self, id, number, type):
        validate_train_number(number)
        self.id = id
        self.number = number
        self.type = type