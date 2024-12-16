from sqlalchemy.orm import relationship
from backend.db import db


class Date(db.Model):
    __tablename__ = 'dates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'), nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey('comps.id'), nullable=False)

    train = relationship("Train", back_populates="dates")
    comp = relationship("Comp", back_populates="dates")

    def __init__(self, date, train_id, comp_id):
        self.date = date
        self.train_id = train_id
        self.comp_id = comp_id