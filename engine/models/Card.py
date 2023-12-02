from main import db


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer(), primary_key=True)
    cardNum = db.Column(db.String(length=20), nullable=False, unique=True)
    cardDate = db.Column(db.String(length=10), nullable=False)
    cardCvv = db.Column(db.String(3), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, cardNum, cardDate, cardCvv, id=None, budget=1000, owner=-1):
        self.id = id
        self.cardNum = cardNum
        self.cardDate = cardDate
        self.cardCvv = cardCvv
        self.budget = budget
        self.owner = owner
