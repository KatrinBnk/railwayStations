from sqlalchemy.orm import relationship

from backend.db import db

class Wagon(db.Model):

    __tablename__ = 'wagons'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey('typeWagon.id'))

    comp = relationship("Comp", back_populates="wagons")
    seats = relationship("Seat", back_populates="wagon")
    type_wagon = relationship("TypeWagon", back_populates="wagons")

    def __init__(self, id, type):
        self.id = id
        self.type = type
