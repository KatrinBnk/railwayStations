from sqlalchemy.orm import relationship
from backend.db import db

class Ticket(db.Model):

    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'))
    date = db.Column(db.Date)
    arrival_info = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    departure_info = db.Column(db.Integer, db.ForeignKey('schedules.id'))
    price = db.Column(db.Integer, nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('staffs.user_id'))
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.passenger_id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    arrival_schedule = relationship("Schedule", foreign_keys=[arrival_info])
    departure_schedule = relationship("Schedule", foreign_keys=[departure_info])
    train = relationship("Train", foreign_keys=[train_id])
    cashier = relationship("Staff", foreign_keys=[cashier_id])
    passenger = relationship("Passenger", foreign_keys=[passenger_id])
    seat_ticket = relationship("SeatsTicket", back_populates="ticket", cascade="all, delete-orphan")
    buyer = relationship("User", foreign_keys=[buyer_id], back_populates='purchased_tickets')

    def __init__(self, train_id, date, arrival_info, departure_info, price, cashier_id,passenger_id, buyer_id):
        self.train_id = train_id
        self.date = date
        self.arrival_info = arrival_info
        self.departure_info = departure_info
        self.price = price
        self.cashier_id = cashier_id
        self.passenger_id = passenger_id
        self.buyer_id = buyer_id

