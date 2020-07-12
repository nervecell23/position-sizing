from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Candlesticks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    ticker = db.Column(db.String(128))
    ask = db.Column(db.Float)
    bid = db.Column(db.Float)
    note = db.Column(db.Integer)

    def __repr__(self):
        return f"<id {self.id}>"

