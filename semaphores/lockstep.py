import time
import random
from threading import Thread, Semaphore


LOOPS = 10
MAX_SLEEP_TIME = 3


class WrappedSemaphore(Semaphore):
    wait = Semaphore.acquire
    signal = Semaphore.release


def thread_A(sem1, sem2):
    for i in range(LOOPS):
        print(f'A{i} perform')
        time.sleep(random.randrange(0, MAX_SLEEP_TIME))

        sem1.signal()
        sem2.wait()


def thread_B(sem1, sem2):
    for i in range(LOOPS):
        print(f'B{i} perform')
        time.sleep(random.randrange(0, MAX_SLEEP_TIME))

        sem2.signal()
        sem1.wait()


sem1 = WrappedSemaphore(0)
sem2 = WrappedSemaphore(0)
workers = [
    Thread(target=thread_A, args=(sem1, sem2)),
    Thread(target=thread_B, args=(sem1, sem2)),
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

