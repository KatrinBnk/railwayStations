from backend.db import db
class Train(db.Model):
    id = db.Column(db.String(4), primary_key=True)
    train_type = db.Column(db.String(50), nullable=False)

    def __init__(self, id, train_type):
        self.id = id
        self.train_type = train_type