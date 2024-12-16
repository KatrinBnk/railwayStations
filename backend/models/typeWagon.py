from backend.db import db


class typeWagons(db.Model):
    id = db.Column(db.Integer, primary_key=True),
    description = db.Column(db.String()),
    conveniences = db.Column(db.String()),
    count_seats = db.Column(db.Integer())

    __table_args__ = (
        db.CheckConstraint(count_seats.in_([14, 36, 54]), name='check_count_seats'),
    )

    def __init__(self, id, description, conveniences, count_seats):
        self.id = id
        self.description = description
        self.conveniences = conveniences
        self.count_seats = count_seats
