import sys
from time import sleep
from Configuration.config import db, sendingSocket, app
from Configuration.exchange import exchangeMoney
from Models.__init__ import Transaction, User, Balance, Product
from threading import Lock


mutex = Lock()

#addTransaction(token, (email, receiverEmail, args['amount'], args['currency'], args['product']))

# Thread that processes transactions
def threadWorker(email, receiver, amount, currency, client_id, product):
    def addTransaction(sender, receiver, amount, currency, state, product):
        # Flask app -> app_context()
        print("HI from threadWorker")  # OVO radi
        with app.app_context():
            transaction = Transaction(sender, receiver, amount, currency, state, product)
            db.session.add(transaction)
            db.session.commit()
        print("DONE")   # Ovo ne radi
        return transaction

    def changeTransactionState(transaction, state):
        if not transaction:
            return
        with app.app_context():
            # merge() gets transaction from DB to local memory
            transaction = db.session.merge(transaction)
            db.session.execute(
                db.select(Transaction).
                filter_by(sender=transaction.sender, receiver=transaction.receiver, amount=transaction.amount,
                          currency=transaction.currency, state="Processing", product=transaction.product).
                order_by(Transaction.id)
            ).scalars().first()
            transaction.state = state
            db.session.commit()

    transaction = None
    try:
        print("Starting thread...", sys.stderr)
        # Ode u funkciju i ne završi je
        transaction = addTransaction(email, receiver, amount, currency, "Processing", product)
        #sleep(10)   # 10 seconds

        print("Starting money exchange...", sys.stderr)
        with app.app_context():
            # Product amount
            temp = db.session.execute(db.select(Product).filter_by(id=product)).one_or_none()
            if temp is None:
                raise Exception("")
            prod = temp[0]
            if prod.amount < amount:
                raise Exception("")

            # Product price in given currency
            prodPrice = prod.price * amount
            if prod.currency != currency:
                prodPrice = exchangeMoney(prodPrice, prod.currency, currency)

            # Sender account
            temp = db.session.execute(db.select(User).filter_by(email=email)).one_or_none()
            if temp is None:
                raise Exception("")

            account = temp[0]
            temp = db.session.execute(
                db.select(Balance).filter_by(accountNumber=account.accountNumber, currency=currency)
            ).one_or_none()
            if temp is None:
                raise Exception("")

            balance = temp[0]
            if balance.amount < prodPrice:
                raise Exception("")

            # Receiver account
            temp = db.session.execute(db.select(User).filter_by(email=receiver)).one_or_none()
            if not temp or not temp[0].verified:
                raise Exception("")

            accountReceiver = temp[0]
            receiverNumber = accountReceiver.accountNumber
            receiverBalance = db.session.execute(
                db.select(Balance).filter_by(accountNumber=receiverNumber, currency=currency)).one_or_none()

            # If receiver doesn't have balance in given currency, create one
            if not receiverBalance:
                receiverBalance = Balance(receiverNumber, prodPrice, currency)
                db.session.add(receiverBalance)
            else:
                receiverBalance[0].amount += prodPrice

            balance.amount -= prodPrice
            if balance.amount == 0:
                db.session.delete(balance)
            db.session.commit()

            prod.amount -= amount
            db.session.commit()

        changeTransactionState(transaction, "Approved")
    except:
        changeTransactionState(transaction, "Denied")
        return
