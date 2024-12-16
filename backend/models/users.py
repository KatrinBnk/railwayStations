from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

from backend.db import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    passenger = relationship("Passenger", back_populates="user", uselist=False)
    staff = relationship("Staff", back_populates="user", uselist=False, cascade="all, delete")
    purchased_tickets = db.relationship('Ticket', back_populates="buyer")
    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)
