from sqlalchemy.orm import relationship

from backend.db import db


class Comp(db.Model):
    __tablename__ = 'comps'

    id = db.Column(db.Integer, primary_key=True)
    wagon_id = db.Column(db.Integer, db.ForeignKey('wagons.id'), primary_key=True)
    number_wagon = db.Column(db.Integer, nullable=False)

    wagons = relationship("Wagon", back_populates="comp")
    dates = relationship("Date", back_populates="comp")

    __table_args__ = (
        db.CheckConstraint('number_wagon between 1 and 15', name='check_number_wagon'),
    )

    def __init__(self, id, wagon_id, number_wagon):
        self.id = id
        self.wagon_id = wagon_id
        self.number_wagon = number_wagon

    def to_dict(self):
        return {
            "id": self.id,
            "wagon_id": self.wagon_id,
            "number_wagon": self.number_wagon
        }
