from Configuration.config import api, jsonify, db, activeTokens, make_response, reqparse, app
from Configuration.exchange import exchangeMoney
from flask_restful import Resource
from Models.__init__ import Transaction, TransactionSchema, Product, Balance, User, CreditCard
from Processes.__init__ import addTransaction

transactionArgs = reqparse.RequestParser()
transactionArgs.add_argument("amount", type=float, help="Amount can't be 0 and it's required", required=True)
transactionArgs.add_argument("currency", type=str, help="Currency is required", required=True)
transactionArgs.add_argument("product", type=int, help="Product ID is required", required=True)


# Get transaction - returns history of transactions for user
# Post transaction - makes new transaction ("buys" product)
class TransactionData(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            email = activeTokens[token]

            # transactionSender - all users
            # transactionReceiver - only admin
            transaction_sender = db.session.execute(db.select(Transaction).filter_by(sender=email)).all()
            transaction_receiver = db.session.execute(
                db.select(Transaction).filter_by(receiver=email, state="Approved")).all()

            transactions = transaction_sender + transaction_receiver
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
            receiver_email = "drs.projekat.tim12@gmail.com"

            if token not in activeTokens.keys():
                return "Please login to continue.", 400
            sender_email = activeTokens[token]

            amount = args['amount']
            if amount <= 0:
                return "Amount must be greater than 0", 400

            currency = args['currency']
            state = 'Processing'
            product_id = args['product']

            # New transaction in "Processing" state (for now)
            transaction = Transaction(sender_email, receiver_email, amount, currency, state, product_id)

            # Product amount
            temp = db.session.execute(db.select(Product).filter_by(id=transaction.product)).one_or_none()
            if temp is None:
                raise Exception("")
            prod = temp[0]
            if prod.amount < transaction.amount:
                raise Exception("")

            # Product price in given currency
            product_price = prod.price * transaction.amount
            if prod.currency != transaction.currency:
                product_price = exchangeMoney(product_price, prod.currency, transaction.currency)

            # Sender (buyer) account
            temp = db.session.execute(db.select(User).filter_by(email=transaction.sender)).one_or_none()
            if temp is None:
                raise Exception("")

            account = temp[0]
            temp = db.session.execute(
                db.select(Balance).filter_by(accountNumber=account.accountNumber, currency=transaction.currency)
            ).one_or_none()
            if temp is None:
                raise Exception("")

            # Check if sender's card is verified
            temp = db.session.execute(
                db.select(CreditCard).filter_by(bankAccountNumber=account.accountNumber)).one_or_none()
            if temp is None:
                raise Exception("")
            card = temp[0]
            if not card.verified:
                raise Exception("")

            # Balance in selected currency
            # If buyer doesn't have enough funds -> Deny transaction
            balance = temp[0]
            if balance.amount < product_price:
                transaction.state = 'Denied'

            # Add new transaction to DB
            db.session.add(transaction)
            addTransaction(token, transaction)

            db.session.commit()

            return "OK", 200
        except Exception as e:
            return 'Error: ' + str(e), 500


api.add_resource(TransactionData, "/transaction/<string:token>")


# For Admin - returns all transactions from all users
class TransactionHistory(Resource):
    def get(self, token):
        try:
            if token not in activeTokens.keys():
                return "Please login to continue.", 400

            # Check if request came from admin
            admin_email = "drs.projekat.tim12@gmail.com"
            if activeTokens[token] != admin_email:
                return "You are not administrator!", 400

            # Get all transactions
            transaction_history = db.session.execute(db.select(Transaction)).all()

            if len(transaction_history) == 0:
                return "There are no transactions", 200

            list = []
            for transaction in transaction_history:
                transaction_schema = TransactionSchema()
                result = transaction_schema.dump(transaction[0])
                list.append(result)

            # Most recent first (bigger ID)
            list.reverse()
            return make_response(jsonify(list), 200)

        except Exception as e:
            return 'Error: ' + str(e), 500


api.add_resource(TransactionHistory, "/transactionHistory/<string:token>")
