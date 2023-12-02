from main import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    seller = db.Column(db.Integer(), db.ForeignKey('user.id'))
    price = db.Column(db.Integer(), nullable=False)
    currency = db.Column(db.String(length=10), nullable=False, default='USD')
    amount = db.Column(db.Float(), nullable=False)
    sellerRef = db.relationship("User", backref="sender", foreign_keys=[seller], lazy='subquery')

    def __init__(self, id=None, seller=-1, price=-1, currency="USD", amount=0):
        self.id = id
        self.seller = seller
        self.price = price
        self.currency = currency
        self.amount = amount
