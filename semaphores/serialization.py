import time
from threading import Thread, Semaphore


class WrappedSemaphore(Semaphore):
    def wait(self):
        self.acquire()

    def signal(self):
        self.release()


def A(sem1, sem2):
    print('A1 perform')
    time.sleep(1)

    sem1.signal()
    sem2.wait()

    print('A2 perform')
    time.sleep(1)


def B(sem1, sem2):
    print('B1 perform')
    time.sleep(1)

    sem2.signal()
    sem1.wait()

    print('B2 perform')
    time.sleep(1)


sem1 = WrappedSemaphore(1)
sem2 = WrappedSemaphore(0)
workers = [
    Thread(target=A, args=(sem1, sem2)),
    Thread(target=B, args=(sem1, sem2))
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

