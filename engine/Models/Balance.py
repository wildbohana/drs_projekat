from Configuration.config import db
from marshmallow import Schema, fields


class Balance(db.Model):
    __tablename__ = "balance"
    pk = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accountNumber = db.Column(db.Integer)  #account that has balance in this currency
    amount = db.Column(db.Float)
    currency = db.Column(db.String(3))

    def __init__(self, accountNumber, amount, currency):
        self.accountNumber = accountNumber
        self.amount = amount
        self.currency = currency


class BalanceSchema(Schema):
    pk = fields.Number()
    accountNumber = fields.Number()
    amount = fields.Number()
    currency = fields.Str()
