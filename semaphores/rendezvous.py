import time
from threading import Thread, Semaphore


class WrappedSemaphore(Semaphore):
    wait = Semaphore.acquire
    signal = Semaphore.release


def thread_A(aArrived, bArrived):
    print('A1 perform')
    time.sleep(1)

    aArrived.signal()
    bArrived.wait()

    print('A2 perform')
    time.sleep(1)


def thread_B(aArrived, bArrived):
    print('B1 perform')
    time.sleep(1)

    bArrived.signal()
    aArrived.wait()

    print('B2 perform')
    time.sleep(1)


aArrived = WrappedSemaphore(0)
bArrived = WrappedSemaphore(0)
workers = [
    Thread(target=thread_A, args=(aArrived, bArrived)),
    Thread(target=thread_B, args=(aArrived, bArrived)),
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

