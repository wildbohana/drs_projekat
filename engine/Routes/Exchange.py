from Configuration.config import Resource, reqparse, api, activeTokens, db, make_response, jsonify
from Models.__init__ import User, Balance
from Configuration.exchange import exchangeMoney


excArgs = reqparse.RequestParser()
excArgs.add_argument("oldCurrency", type=str, help="Old currency field is required", required=True)
excArgs.add_argument("newCurrency", type=str, help="New currency field is required", required=True)
excArgs.add_argument("oldValue", type=float, help="Old value field is required", required=True)


# Get exchange - checks value of exchange
# Post exchange - does permanent exchange
class Exchange(Resource):
    def get(self, token):
        try:
            args = excArgs.parse_args()
            ret = exchangeMoney(args["oldValue"], args["oldCurrency"], args["newCurrency"])
            return make_response(jsonify({"value": ret}), 200)
        except Exception as e:
            return "Error: " + str(e), 400

    def post(self, token):
        try:
            args = excArgs.parse_args()
            if token not in activeTokens.keys():
                return "Please login to continue", 400
            email = activeTokens[token]

            temp = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if temp is None:
                return "User doesnt exist!", 400

            if args["oldValue"] <= 0:
                return "Values must be greater than 0", 400

            account = temp[0]
            balances = db.session.execute(db.select(Balance).filter_by(accountNumber=account.accountNumber)).all()
            if not balances:
                return "You dont have any state", 400

            oldBalance, newBalance = None, None
            for temp in balances:
                balance = temp[0]
                if balance.currency == args["oldCurrency"]:
                    oldBalance = balance
                elif balance.currency == args["newCurrency"]:
                    newBalance = balance

            if oldBalance is None:
                return "You don't have any money in " + args["oldCurrency"], 400

            if oldBalance.amount < args["oldValue"]:
                return "You don't have enough money in " + args["oldCurrency"], 400

            if newBalance is None:
                newBalance = Balance(account.accountNumber, 0, args["newCurrency"])
                db.session.add(newBalance)
                db.session.commit()

            oldBalance.amount -= args["oldValue"]
            if oldBalance.amount == 0:
                db.session.delete(oldBalance)
                db.session.commit()

            newBalance.amount += exchangeMoney(args["oldValue"], args["oldCurrency"], args["newCurrency"])
            db.session.commit()
            return "OK", 200
        except Exception as e:
            return "Error:" + str(e), 400


api.add_resource(Exchange, "/exchange/<string:token>")
