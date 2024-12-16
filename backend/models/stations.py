from sqlalchemy.orm import relationship

from backend.db import db


class Station(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(100))

    staffs = relationship("Staff", back_populates="station", cascade="all, delete")
    schedules = relationship("Schedule", back_populates="station", cascade="all, delete")

    __table_args__ = (
        db.CheckConstraint('id BETWEEN 1000000 AND 9999999', name='check_station_code'),
    )

    def __init__(self, id, name, city):
        self.id = id
        self.name = name
        self.city = city

    def to_dict(self):
        return {
            "station_id": self.id,
            "name": self.name,
            "city": self.city
        }
