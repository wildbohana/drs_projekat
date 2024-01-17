from Configuration.config import *
from flask_restful import Resource
from Models.__init__ import CreditCard, CreditCardSchema, User, Balance
from flask import request


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
        card_number = args['cardNumber']
        expiration_date = args['expirationDate']
        cvv = args['cvv']
        amount = args['amount']
        user_name = args['userName']

        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            # Get info on currently logged in account
            account = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if account[0].cardNumber is not None:
                return "You already have a credit card", 400

            # Create the credit card
            card = CreditCard(card_number, user_name, expiration_date, cvv, amount, account[0].accountNumber)
            db.session.add(card)
            db.session.commit()

            # Verify account
            account[0].verified = True
            account[0].cardNumber = card_number

            # Create balance in RSD for this account (initially 0)
            db.session.add(Balance(account[0].accountNumber, 0, "RSD"))
            db.session.commit()
            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(Card, "/card/<string:token>")


# Verify credit card (admin only)
verifyCardArgs = reqparse.RequestParser()
verifyCardArgs.add_argument("cardNumber", type=str, help="Card Number is required", required=True)

class VerifyCard(Resource):
    def post(self):
        #args = verifyCardArgs.parse_args()
        data = request.get_json()
        card_number = data['cardNumber']
        print("vc", card_number)

        try:
            # Get info on credit card
            temp = db.session.execute(db.select(CreditCard).filter_by(cardNumber=card_number)).one_or_none()
            if temp is None:
                return "That card doesn't exist", 400
            card = temp[0]
            if card.verified:
                return "That card is already verified", 400

            # Verify the credit card
            card.verified = True
            db.session.add(card)
            db.session.commit()

            return "OK", 200
        except Exception as e:
            return "Error: " + str(e), 400

    # Get all unverified cards
    def get(self):
        try:
            # Get info on credit card
            cards = db.session.execute(db.select(CreditCard).filter_by(verified=False)).all()
            if len(cards) == 0:
                return "All cards are verified", 200

            list = []
            for card in cards:
                cards_schema = CreditCardSchema()
                result = cards_schema.dump(card[0])
                list.append(result)

            return make_response(jsonify(list), 200)

        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(VerifyCard, "/verifyCard")

"""

class VerifiedCard(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]
            # Get info on credit card
            card = db.session.execute(db.select(CreditCard).filter_by(email=email, verified=True)).one_or_none()

            if card is None:
                return jsonify(message="Card not verified"), 200

            cards_schema = CreditCardSchema()
            result = cards_schema.dump(card[0])

            return make_response(jsonify(result), 200)

        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(VerifyCard, "/getUserCard/<string:token>")
"""