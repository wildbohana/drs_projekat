from marshmallow import Schema, fields
from Configuration.config import db


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.String(64))
    receiver = db.Column(db.String(64))  # admin
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))
    state = db.Column(db.String(32))     # Processing, Approved, Denied
    product = db.Column(db.Integer)      # Product ID

    def __init__(self, sender: object, receiver: object, amount: object, currency: object, state: object, product: object) -> object:
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.currency = currency
        self.state = state
        self.product = product


class TransactionSchema(Schema):
    id = fields.Number()
    sender = fields.Str()
    receiver = fields.Str()
    amount = fields.Float()
    currency = fields.Str()
    state = fields.Str()
    product = fields.Integer()
