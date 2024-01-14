import sys
import threading
from time import sleep
from Configuration.config import db, app, transaction_queue
from Configuration.exchange import exchangeMoney
from Configuration.emails import sendEmail
from Models.__init__ import Transaction, User, Balance, Product, CreditCard


# Open thread for transaction
def openThread():
    thread = threading.Thread(target=processTransactions)
    thread.start()


def processTransactions():
    #print("HI FROM THREAD")
    #sleep(60)
    sleep(1)

    email_subject = "New transactions"
    email_body = ""

    with app.app_context():
        for transaction in transaction_queue:
            #print(transaction.product)
            temp = processOneTransaction(transaction)
            email_body += f"Transaction details:\nProduct ID: {temp.product}\nBuyer email: {temp.sender}\nAmount: {temp.amount}\nCurrency: {temp.currency}\nState: {temp.state}\n"

    if email_body != "":
        sendEmail(email_subject, email_body)

    transaction_queue.clear()


# Thread that processes transactions
def processOneTransaction(transaction: Transaction):
    # Helper function
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

    # Real function body
    try:
        print("Starting transaction...", sys.stderr)
        with app.app_context():
            db.session.add(transaction)
            db.session.commit()

        print("Starting money exchange...", sys.stderr)
        with app.app_context():
            # Product amount
            print(transaction.product)
            temp = db.session.execute(db.select(Product).filter_by(id=transaction.product)).one_or_none()   #???
            if temp is None:
                raise Exception("")
            prod = temp[0]
            if prod.amount < transaction.amount:
                raise Exception("")

            # Product price in given currency
            prodPrice = prod.price * transaction.amount
            if prod.currency != transaction.currency:
                prodPrice = exchangeMoney(prodPrice, prod.currency, transaction.currency)

            # Sender account
            temp = db.session.execute(db.select(User).filter_by(email=transaction.sender)).one_or_none()
            if temp is None:
                raise Exception("")

            account = temp[0]
            temp = db.session.execute(
                db.select(Balance).filter_by(accountNumber=account.accountNumber, currency=transaction.currency)
            ).one_or_none()
            if temp is None:
                raise Exception("")

            balance = temp[0]
            if balance.amount < prodPrice:
                raise Exception("")

            # Check if sender's card is verified
            temp = db.session.execute(db.select(CreditCard).filter_by(bankAccountNumber=account.accountNumber)).one_or_none()
            if temp is None:
                raise Exception("")
            card = temp[0]
            if not card.verified:
                raise Exception("")

            # Receiver account
            temp = db.session.execute(db.select(User).filter_by(email=transaction.receiver)).one_or_none()
            if not temp or not temp[0].verified:
                raise Exception("")

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
            db.session.commit()

            prod.amount -= transaction.amount
            db.session.commit()

        changeTransactionState(transaction, "Approved")
        print(transaction.state)
        return transaction
    except:
        changeTransactionState(transaction, "Denied")
        print(transaction.state)
        return transaction
