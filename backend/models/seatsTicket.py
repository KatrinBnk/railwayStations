from sqlalchemy.orm import relationship

from backend.db import db
from sqlalchemy import Enum


class SeatsTicket(db.Model):
    __tablename__ = 'seatsTickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seat_id = db.Column(db.Integer, db.ForeignKey('seats.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    ticket_state = db.Column(Enum('забронирован', 'выкуплен', 'запрос на возврат', name="TicketState"), nullable=False)

    seat = relationship("Seat", back_populates="seats_tickets")
    ticket = relationship("Ticket", back_populates="seat_ticket", cascade="all, delete")

    def __init__(self, seat_id, ticket_id, ticket_state, id=None):
        if id is not None:
            self.id = id
        self.seat_id = seat_id
        self.ticket_id = ticket_id
        self.ticket_state = ticket_state
