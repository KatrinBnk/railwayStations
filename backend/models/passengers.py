from sqlalchemy.orm import relationship

from backend.db import db


class Passenger(db.Model):
    __tablename__ = 'passengers'

    passenger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=False)
    passport = db.Column(db.String(20), nullable=False, unique=True)

    __table_args__ = (
        db.CheckConstraint(
            "passport ~ '^[0-9]{4} [0-9]{6}$'",
            name='check_passport_format'
        ),
    )

    user = relationship("User", back_populates="passenger", uselist=False)
    tickets = relationship("Ticket", back_populates="passenger")

    def __init__(self, last_name, first_name, middle_name, passport, user_id=None):
        if user_id is not None:
            self.user_id = user_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.passport = passport
