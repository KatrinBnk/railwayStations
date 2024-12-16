from sqlalchemy.orm import relationship

from backend.db import db


class Staff(db.Model):

    __tablename__ = 'staffs'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    position = db.Column(db.String(100), nullable=False)

    user = relationship("User", back_populates="staff", uselist=False)
    station = relationship("Station", back_populates="staffs")
    tickets = relationship("Ticket", back_populates="cashier")


    def __init__(self, user_id, station_id, last_name, first_name, middle_name, position):
        self.station_id = station_id
        self.user_id = user_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.position = position
