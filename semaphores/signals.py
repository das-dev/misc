import time
from threading import Thread, Semaphore


def A(sem):
    print('A waiting...')
    sem.acquire()
    print('Signal received')


def B(sem):
    time.sleep(5)
    print('B signal')
    sem.release()


sem = Semaphore(0)
workers = [
    Thread(target=A, args=(sem,)),
    Thread(target=B, args=(sem,))
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

