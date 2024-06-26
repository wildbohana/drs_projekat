from Configuration.config import db
from marshmallow import Schema, fields


# Card ID == card number
class CreditCard(db.Model):
    __tablename__ = 'credit_card'
    cardNumber = db.Column(db.String(16), primary_key=True)
    userName = db.Column(db.String(32))
    expirationDate = db.Column(db.String(5))
    cvv = db.Column(db.Integer)
    amount = db.Column(db.Float)    #Amount of money in RSD
    bankAccountNumber = db.Column(db.String(10))
    verified = db.Column(db.Boolean, default=False)


    def __init__(self, cardNumber, userName, expirationDate, cvv, amount, bankAccountNumber):
        self.cardNumber = cardNumber
        self.userName = userName
        self.expirationDate = expirationDate
        self.cvv = cvv
        self.amount = amount
        self.bankAccountNumber = bankAccountNumber
        self.verified = False


class CreditCardSchema(Schema):
    cardNumber = fields.Number()
    userName = fields.Str()
    expirationDate = fields.Str()
    cvv = fields.Number()
    amount = fields.Float()
    bankAccountNumber = fields.Str()
    verified = fields.Boolean()
