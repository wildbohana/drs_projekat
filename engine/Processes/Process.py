from multiprocessing import Process, Queue
from threading import Thread
from Processes.Thread import *

# Dict with tokens and PIDs
# TODO probably remove, I only need a few threads, and not their tokens
activeProcesses = {}


# Opens thread when transaction starts
def processWorker(q: Queue):
    while True:
        if q.qsize() == 0:
            sleep(10)       # 10 seconds
            continue

        transaction = q.get()
        Thread(target=threadWorker, args=transaction).start()


# Opens new process for user (token)
def openProcess(token, client_id):
    q = Queue()
    temp = Process(target=processWorker, args=[q])
    temp.start()
    activeProcesses[token] = (temp, q, client_id)

    # Remove or keep?
    try:
        with app.app_context():
            db.session.execute(db.select(User).filter_by(email="drs.projekat.tim12@gmail.com")).one_or_none()

    except Exception as e:
        print(e)


# Closes user's process (token)
def closeProcess(token):
    if not activeProcesses[token]:
        print("ERROR: Process is not active")
    process, queue, client_id = activeProcesses.pop(token)
    process.terminate()


# Adds transaction to the process queue
def addTransaction(token, transaction: tuple):
    if not activeProcesses[token]:
        print("ERROR: Process is not active")

    process, queue, client_id = activeProcesses[token]
    queue.put(transaction + (client_id,))
    print("HI FROM PROCESS.PY")
