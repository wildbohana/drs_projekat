from flask_login import UserMixin
from main import db


def load_user(user_id):
    return User.query.get(int(user_id))


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
