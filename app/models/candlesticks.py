from app import db

class Candlesticks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime)
    ticker = db.Column(db.String(128))
    ask = db.Column(db.Float)
    bid = db.Column(db.Float)

    def __init__(self, id, ticker, dt, ask, bid):
        self.dt = dt
        self.ticker = ticker
        self.ask = ask
        self.bid = bid

    def __repr__(self):
        return f"<id {self.id}>"

