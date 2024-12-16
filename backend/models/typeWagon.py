from sqlalchemy.orm import relationship

from backend.db import db


class TypeWagon(db.Model):

    __tablename__ = 'typeWagon'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    conveniences = db.Column(db.String())
    count_seats = db.Column(db.Integer())

    wagons = relationship("Wagon", back_populates="type_wagon")

    __table_args__ = (
        db.CheckConstraint(count_seats.in_([18, 36, 54]), name='check_count_seats'),
    )

    def __init__(self, id, description, conveniences, count_seats):
        self.id = id
        self.description = description
        self.conveniences = conveniences
        self.count_seats = count_seats
