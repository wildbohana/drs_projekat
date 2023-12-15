from Configuration.config import api, jsonify, db, activeTokens, make_response, reqparse
from flask_restful import Resource
from Models.__init__ import Transaction, TransactionSchema
from Processes.__init__ import addTransaction


transactionArgs = reqparse.RequestParser()
transactionArgs.add_argument("amount", type=float, help="Amount can't be 0 and it's required", required=True)
transactionArgs.add_argument("currency", type=str, help="Currency is required", required=True)
transactionArgs.add_argument("product", type=int, help="Product ID is required", required=True)

# Get transaction - returns history of transactions for user
# Post transaction - makes new transaction (buys product)
class TransactionProfile(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            # transactionSender - all users
            # transactionReceiver - only admin
            transactionSender = db.session.execute(db.select(Transaction).filter_by(sender=email)).all()
            transactionReceiver = db.session.execute(
                db.select(Transaction).filter_by(receiver=email, state="Approved")).all()

            transactions = transactionSender + transactionReceiver
            if len(transactions) == 0:
                return "There are no transactions", 200

            list = []
            for transaction in transactions:
                transaction_schema = TransactionSchema()
                result = transaction_schema.dump(transaction[0])
                list.append(result)
            return make_response(jsonify(list), 200)
        except Exception as e:
            return 'Error: ' + str(e), 500

    def post(self, token):
        try:
            args = transactionArgs.parse_args()
            receiverEmail = "drs.projekat.tim12@gmail.com"

            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            if args["amount"] <= 0:
                return "Amount must be greater than 0", 400

            addTransaction(token, (email, receiverEmail, args['amount'], args['currency'], args['product']))
            return "OK", 200
        except Exception as e:
            return 'Error: ' + str(e), 500


api.add_resource(TransactionProfile, "/transaction/<string:token>")

#TODO get-all chronologically (for admin)
#TODO every 60s process all transactions (from processing to approved)
