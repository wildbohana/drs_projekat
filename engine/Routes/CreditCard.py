from Configuration.config import *
from flask_restful import Resource
from Models.__init__ import CreditCard, User, Balance
from Configuration.exchange import exchangeMoney

cardArgs = reqparse.RequestParser()
cardArgs.add_argument("cardNumber", type=str, help="Card Number is required", required=True)
cardArgs.add_argument("expirationDate", type=str, help="Date is required", required=True)
cardArgs.add_argument("cvv", type=int, help="CVV is required", required=True)
cardArgs.add_argument("userName", type=str, help="Name and surname are required", required=True)


# Adding credit card (verifying the account)
class Card(Resource):
    def post(self, token):
        args = cardArgs.parse_args()
        cardNumber, expirationDate, cvv, userName = (args['cardNumber'], args['expirationDate'],
                                                     args['cvv'], args['userName'])
        USDInRSD = exchangeMoney(1, "USD", "RSD")

        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            # Get info on currently logged in account
            account = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()[0]
            if account.cardNumber is not None:
                return "You already have a credit card", 400

            # Find the credit card
            card = db.session.execute(db.select(CreditCard).filter_by(
                cardNumber=cardNumber, expirationDate=expirationDate,
                cvv=cvv, userName=userName)).one_or_none()
            # Ovo sa [0] radi kada ima nečega, a ne radi kada nema ničega

            if not card:
                return "Card does not exist", 404
            if card.amount < USDInRSD:
                return "You don't have enough money on your card", 400

            card.amount -= USDInRSD
            account.verified = True
            account.cardNumber = cardNumber
            db.session.add(Balance(account.accountNumber, 0, "RSD"))
            db.session.commit()
            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(Card, "/card/<string:token>")
