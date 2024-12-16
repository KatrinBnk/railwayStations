from sqlalchemy.orm import relationship

from backend.db import db


class Seat(db.Model):
    __tablename__ = 'seats'

    id = db.Column(db.Integer, primary_key=True)
    wagon_id = db.Column(db.Integer, db.ForeignKey('wagons.id'))
    number_seat = db.Column(db.Integer)
    type_seat = db.Column(db.String)

    wagon = relationship("Wagon", back_populates="seats")
    seats_tickets = relationship("SeatsTicket", back_populates="seat")

    __table_args__ = (
        db.CheckConstraint(type_seat.in_(['верхнее', 'нижнее', 'верхнее боковое', 'нижнее боковое']), name='check_type_seat'),
    )

    def __init__(self, id, wagon_id, number_seat, type_seat):
        self.id = id
        self.wagon_id = wagon_id
        self.number_seat = number_seat
        self.type_seat = type_seat
