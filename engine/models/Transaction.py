from sqlalchemy import text
from enum import Enum
from main import db
from datetime import datetime


class TransactionState(Enum):
    PROCESSING = "PROCESSING"
    ACCEPTED = "ACCEPTED"
    DENIED = "DENIED"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer(), db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer(), db.ForeignKey('user.id'))
    amount = db.Column(db.Integer(), nullable=False)
    state = db.Column(db.Enum(TransactionState), nullable=False)
    timeCreated = db.Column(db.DateTime(), default=text("datetime('now','localtime')"))
    currency = db.Column(db.String(length=10), nullable=False, default='USD')
    senderRef = db.relationship("User", backref="sender", foreign_keys=[sender], lazy='subquery')
    receiverRef = db.relationship("User", backref="receiver", foreign_keys=[receiver], lazy='subquery')

    def __init__(self, sender, receiver, amount, currency, id=-1):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.state = TransactionState.PROCESSING
        self.timeCreated = datetime.now()
        self.currency = currency
