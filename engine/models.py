from flask_login import UserMixin
from sqlalchemy import text
from enum import Enum
from datetime import datetime
from main import db


# Error jer zahteva db, a db zahteva User
# A i svakako se ne može samo tako importovati PostgreSQL baza


def load_user(user_id):
    return User.query.get(int(user_id))


# TODO: dodaj svim klasama ToJSON() metodu ??
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=20), nullable=False)
    lastName = db.Column(db.String(length=20), nullable=False)
    address = db.Column(db.String(length=80), nullable=False)
    city = db.Column(db.String(length=20), nullable=False)
    country = db.Column(db.String(length=20), nullable=False)
    phone = db.Column(db.String(length=10), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=20), nullable=False)
    verified = db.Column(db.Boolean(), default=False, nullable=False)
    card = db.relationship("Card", backref="owned_user", lazy='subquery')
    balance = db.relationship('Account_balance', backref='owned_user', lazy=True)
    currency = db.relationship('Account_currency', backref='owned_user', lazy=True)

    def __init__(self, firstname, lastname, address, city, country, phone, email, password, verified=False, id=None):
        self.id = id
        self.firstName = firstname
        self.lastName = lastname
        self.address = address
        self.city = city
        self.country = country
        self.phone = phone
        self.email = email
        self.password = password
        self.verified = verified

    def __iter__(self):
        return iter([self.id, self.email, self.firstName, self.lastName,
                     self.address, self.city, self.country, self.phone,
                     self.password, self.verified, self.card])

    def check_password_correction(self, attempted_password):
        if self.password == attempted_password:
            return True
        else:
            return False


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer(), primary_key=True)
    cardNum = db.Column(db.String(length=20), nullable=False, unique=True)
    cardDate = db.Column(db.String(length=10), nullable=False)
    cardCvv = db.Column(db.String(3), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __init__(self, cardNum, cardDate, cardCvv, id=None, budget=1000, owner=-1):
        self.id = id
        self.cardNum = cardNum
        self.cardDate = cardDate
        self.cardCvv = cardCvv
        self.budget = budget
        self.owner = owner


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False, default='Undefined')
    seller = db.Column(db.Integer(), db.ForeignKey('users.id'))
    price = db.Column(db.Integer(), nullable=False)
    currency = db.Column(db.String(length=10), nullable=False, default='USD')
    amount = db.Column(db.Float(), nullable=False)
    sellerRef = db.relationship("User", backref="sender", foreign_keys=[seller], lazy='subquery')

    def __init__(self, id=None, name="Undefined", seller=-1, price=-1, currency="USD", amount=0):
        self.id = id
        self.name = name
        self.seller = seller
        self.price = price
        self.currency = currency
        self.amount = amount


class TransactionState(Enum):
    PROCESSING = "PROCESSING"
    ACCEPTED = "ACCEPTED"
    DENIED = "DENIED"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer(), db.ForeignKey('users.id'))
    receiver = db.Column(db.Integer(), db.ForeignKey('users.id'))
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
