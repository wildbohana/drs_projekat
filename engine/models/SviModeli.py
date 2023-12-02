# TODO: obriši kasnije ovaj fajl skroz

from flask_login import UserMixin
from main import db
from sqlalchemy import text
from enum import Enum


def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
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

    def __repr__(self):
        return f'User {self.email}'

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
    id = db.Column(db.Integer(), primary_key=True)
    cardNum = db.Column(db.String(length=20), nullable=False, unique=True)
    cardDate = db.Column(db.String(length=10), nullable=False)
    cardCvv = db.Column(db.String(3), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


class TransactionState(Enum):
    PROCESSING = "PROCESSING"
    ACCEPTED = "ACCEPTED"
    DENIED = "DENIED"


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sender = db.Column(db.Integer(), db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer(), db.ForeignKey('user.id'))
    amount = db.Column(db.Integer(), nullable=False)
    state = db.Column(db.Enum(TransactionState), nullable=False)
    timeCreated = db.Column(db.DateTime(), default=text("datetime('now','localtime')"))
    currency = db.Column(db.String(length=10), nullable=False, default='USD')
    senderRef = db.relationship("User", backref="sender", foreign_keys=[sender], lazy='subquery')
    receiverRef = db.relationship("User", backref="receiver", foreign_keys=[receiver], lazy='subquery')


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    seller = db.Column(db.Integer(), db.ForeignKey('user.id'))
    price = db.Column(db.Integer(), nullable=False)
    currency = db.Column(db.String(length=10), nullable=False, default='USD')
    amount = db.Column(db.Float(), nullable=False)
    sellerRef = db.relationship("User", backref="sender", foreign_keys=[seller], lazy='subquery')
