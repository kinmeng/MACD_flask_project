from app_local import db
from sqlalchemy.dialects.postgresql import JSON
import datetime

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(JSON)
    stock_name = db.Column(db.String)
    stock_ticker = db.Column(db.String)
    date_generated = db.Column(db.Date(), default=datetime.datetime.utcnow)

    def __init__(self, result, stock_name, stock_ticker):
        self.result = result
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        
      

    def __repr__(self):
        return '<id {}>'.format(self.id)
