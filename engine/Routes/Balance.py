from Configuration.config import *
from flask_restful import Resource, reqparse
from Models import CreditCard
from Models.__init__ import User, Balance, BalanceSchema
from Configuration import exchange

# Post arguments
accountBalanceArgs = reqparse.RequestParser()
accountBalanceArgs.add_argument("amount", type=float, help="Value is required", required=True)
accountBalanceArgs.add_argument("currency", type=str, help="Currency is required", required=True)


# Account balance get - show balance in all currencies
# Account balance post - add money from credit card to account balance
class AccountBalance(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            temp = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if temp is None:
                return "Error, no account found", 404
            account = temp[0]
            if not account.verified:
                return "Please verify first", 400

            balances = db.session.execute(db.select(Balance).filter_by(accountNumber=account.accountNumber)).all()
            if balances is None:
                return "Account doesn't have any balance", 400

            list = []
            for balance in balances:
                balance_schema = BalanceSchema()
                result = balance_schema.dump(balance[0])
                list.append(result)
            return make_response(jsonify(list), 200)
        except Exception as e:
            return "Error: " + str(e), 400

    def post(self, token):
        args = accountBalanceArgs.parse_args()
        amount = args['amount']
        currency = args['currency']

        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            if amount <= 0:
                return "Amount must be greater than 0", 400

            temp = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if temp is None:
                return "Error, no account found", 404

            account = temp[0]
            if not account.verified:
                return "Please verify first", 400

            user_accounts = db.session.execute(db.select(Balance).filter_by(accountNumber=account.accountNumber)).all()
            target_balance = None

            # Check if user has balance in that currency
            for balance in user_accounts:
                if balance[0].currency == currency:
                    target_balance = balance[0]

            # If not, create new balance
            if target_balance is None:
                target_balance = Balance(account.accountNumber, 0, currency)
                db.session.add(target_balance)
                db.session.commit()

            if target_balance:
                card = db.session.execute(db.select(CreditCard).filter_by(cardNumber=account.cardNumber)).one_or_none()

                # Convert amount to RSD
                amount_in_rsd = exchange.exchangeMoney(amount, currency, "RSD")
                if card[0].amount < amount_in_rsd:
                    return "You don't have enough money on credit card", 400
                card[0].amount -= amount_in_rsd

                target_balance.amount += amount
                db.session.commit()
                return "OK", 200
            else:
                return "Error", 400
        except Exception as e:
            return "Error: " + str(e), 400


api.add_resource(AccountBalance, "/accountBalance/<string:token>")
