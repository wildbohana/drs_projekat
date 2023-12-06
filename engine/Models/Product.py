from marshmallow import Schema, fields
from Configuration.config import db


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Float)
    currency = db.Column(db.String(3))
    amount = db.Column(db.Float)

    def __init__(self, name, price, currency, amount):
        self.name = name
        self.price = price
        self.amount = amount
        self.currency = currency
        self.amount = amount


class ProductSchema(Schema):
    id = fields.Number()
    name = fields.Str()
    price = fields.Float()
    currency = fields.Str()
    amount = fields.Float()
