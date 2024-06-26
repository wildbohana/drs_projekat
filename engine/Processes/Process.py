from multiprocessing import Process, Queue
from threading import Thread
from Processes.Thread import *
from Configuration.emails import sendEmail
from Configuration.config import emailQueue as qe

# Dict with tokens and PIDs
activeProcesses = {}


# Sends email when query for process is empty
def TransactionsEmail():
    email_subject = "New transactions"
    email_body = ""

    while qe.empty() is False:
        pt = qe.get()
        email_body += (f"Transaction details:\n"
                       f"Product ID: {pt.product}\n"
                       f"Buyer email: {pt.sender}\n"
                       f"Amount: {pt.amount}\n"
                       f"Currency: {pt.currency}\n"
                       f"State: {pt.state}\n"
                       f"\n-----------\n\n")

    if email_body is not "":
        sendEmail(email_subject, email_body)


# Opens thread when transaction starts
def processWorker(q: Queue):
    while True:
        if q.qsize() == 0:
            sleep(1)
            TransactionsEmail()

            # Process all from queue, then sleep 60s
            sleep(60)
            continue

        sleep(1)
        transaction = q.get()
        Thread(target=threadWorker, args=(transaction,)).start()


# Opens new process for user (token)
def openProcess(token):
    q = Queue()     # Queue for pending transactions
    temp = Process(target=processWorker, args=[q])
    temp.start()
    activeProcesses[token] = (temp, q, qe)


# Closes user's process (token)
def closeProcess(token):
    if not activeProcesses[token]:
        print("ERROR: Process is not active")
    process, queue = activeProcesses.pop(token)
    process.terminate()


# Adds transaction to the process queue
def addTransaction(token, transaction: Transaction):
    if not activeProcesses[token]:
        print("ERROR: Process is not active")

    process, queue, equeue = activeProcesses[token]
    queue.put(transaction)
