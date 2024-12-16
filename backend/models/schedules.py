from sqlalchemy.orm import relationship

from backend.db import db


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)
    day_in = db.Column(db.Integer, nullable=False)

    train = relationship("Train", back_populates="schedules")
    station = relationship("Station", back_populates="schedules")
    arrival = relationship("Ticket", back_populates="arrival_schedule", foreign_keys="Ticket.arrival_info",
                           cascade="all, delete-orphan")
    departure = relationship("Ticket", back_populates="departure_schedule", foreign_keys="Ticket.departure_info",
                             cascade="all, delete-orphan")

    def __init__(self, train_id, station_id, arrival_time, departure_time, day_in, id=None):
        if id is not None:
            self.id = id
        self.train_id = train_id
        self.station_id = station_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.day_in = day_in
