from Configuration.config import db
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(64), unique=True)   # Also - User ID
    password = db.Column(db.String(64))
    firstName = db.Column(db.String(32))
    lastName = db.Column(db.String(32))
    address = db.Column(db.String(64))
    city = db.Column(db.String(32))
    state = db.Column(db.String(32))
    phoneNumber = db.Column(db.String(16))
    verified = db.Column(db.Boolean, default=False)
    accountNumber = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardNumber = db.Column(db.String(20))

    def __init__(self, firstName, lastName, address, city, state, phoneNumber, email, password, verified=False):
        self.firstName = firstName
        self.lastName = lastName
        self.address = address
        self.city = city
        self.state = state
        self.phoneNumber = phoneNumber
        self.email = email
        self.password = password
        self.verified = verified


class UserSchema(Schema):
    email = fields.Str()
    password = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    phoneNumber = fields.Str()
    verified = fields.Boolean()
    accountNumber = fields.Number()
    cardNumber = fields.Str()
