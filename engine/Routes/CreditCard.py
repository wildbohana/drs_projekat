from Configuration.config import *
from flask_restful import Resource
from Models.__init__ import CreditCard, User, Balance


#TODO administrator treba da odobri dodavanje kartice na nalog (ovo na frontu?)
cardArgs = reqparse.RequestParser()
cardArgs.add_argument("cardNumber", type=str, help="Card Number is required", required=True)
cardArgs.add_argument("expirationDate", type=str, help="Date is required", required=True)
cardArgs.add_argument("cvv", type=int, help="CVV is required", required=True)
cardArgs.add_argument("amount", type=float, help="Amount in RSD is required", required=True)
cardArgs.add_argument("userName", type=str, help="Name and surname are required", required=True)


# Adding credit card (verifying the account)
class Card(Resource):
    def post(self, token):
        args = cardArgs.parse_args()
        cardNumber = args['cardNumber']
        expirationDate = args['expirationDate']
        cvv = args['cvv']
        amount = args['amount']
        userName = args['userName']

        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            # Get info on currently logged in account
            account = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if account[0].cardNumber is not None:
                return "You already have a credit card", 400

            # Create the credit card
            card = CreditCard(cardNumber, userName, expirationDate, cvv, amount, account[0].accountNumber)
            db.session.add(card)
            db.session.commit()

            # Verify account
            account[0].verified = True
            account[0].cardNumber = cardNumber

            # Create balance in RSD for this account (initially 0)
            db.session.add(Balance(account[0].accountNumber, 0, "RSD"))
            db.session.commit()
            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(Card, "/card/<string:token>")
