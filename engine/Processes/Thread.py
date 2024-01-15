import sys
from time import sleep
from Configuration.config import db, app
from Configuration.exchange import exchangeMoney
from Models.__init__ import Transaction, User, Balance, Product
from threading import Lock


mutex = Lock()


# Thread that processes transactions
def threadWorker(transaction):
    # Delete and add new one
    def changeTransactionState(current: Transaction, state):
        if not current:
            return
        with app.app_context():
            # merge() gets transaction from DB to local memory
            temp = db.session.execute(
                db.select(Transaction).
                filter_by(sender=current.sender, receiver=current.receiver, amount=current.amount,
                          currency=current.currency, state='Processing', product=current.product).
                order_by(Transaction.id)
            ).scalars().first()
            db.session.delete(temp)

            current.state = state

            db.session.add(current)
            db.session.commit()
            print("New transaction added to database")

    """
    # Helper function
    # Dupli upis u bazu -_-
    def changeTransactionState(tr, state):
        if not tr:
            return
        with app.app_context():
            # merge() gets transaction from DB to local memory
            tr = db.session.merge(tr)
            db.session.execute(
                db.select(Transaction).
                filter_by(sender=tr.sender, receiver=tr.receiver, amount=tr.amount,
                          currency=tr.currency, state="Processing", product=tr.product).
                order_by(Transaction.id)
            ).scalars().first()
            tr.state = state
            db.session.commit()
    """

    # Real function
    try:
        print("Starting thread...", sys.stderr)

        print("Starting money exchange...", sys.stderr)
        with app.app_context():
            # Product amount
            temp = db.session.execute(db.select(Product).filter_by(id=transaction.product)).one_or_none()   # GREŠKA!
            if temp is None:
                raise Exception("prod am")
            prod = temp[0]
            if prod.amount < transaction.amount:
                raise Exception("prod am")

            # Product price in given currency
            prodPrice = prod.price * transaction.amount
            if prod.currency != transaction.currency:
                prodPrice = exchangeMoney(prodPrice, prod.currency, transaction.currency)

            # Sender account
            temp = db.session.execute(db.select(User).filter_by(email=transaction.sender)).one_or_none()
            if temp is None:
                raise Exception("acc")

            account = temp[0]
            temp = db.session.execute(
                db.select(Balance).filter_by(accountNumber=account.accountNumber, currency=transaction.currency)
            ).one_or_none()
            if temp is None:
                raise Exception("balance")

            balance = temp[0]
            if balance.amount < prodPrice:
                raise Exception("balance2")

            # Receiver account
            temp = db.session.execute(db.select(User).filter_by(email=transaction.receiver)).one_or_none()
            if not temp or not temp[0].verified:
                raise Exception("receiver")

            accountReceiver = temp[0]
            receiverNumber = accountReceiver.accountNumber
            receiverBalance = db.session.execute(
                db.select(Balance).filter_by(accountNumber=receiverNumber, currency=transaction.currency)).one_or_none()

            # If receiver doesn't have balance in given currency, create one
            if not receiverBalance:
                receiverBalance = Balance(receiverNumber, prodPrice, transaction.currency)
                db.session.add(receiverBalance)
            else:
                receiverBalance[0].amount += prodPrice

            balance.amount -= prodPrice
            if balance.amount == 0:
                db.session.delete(balance)

            prod.amount -= transaction.amount
            db.session.commit()

        changeTransactionState(transaction, "Approved")
    except Exception as e:
        print(str(e))
        changeTransactionState(transaction, "Denied")
        return
