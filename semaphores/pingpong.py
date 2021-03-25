import time
from threading import Semaphore, Thread


def ping(forward, backward):
    while True:
        forward.acquire()
        print('ping')
        time.sleep(1)
        backward.release()

def pong(forward, backward):
    while True:
        backward.acquire()
        print('pong')
        time.sleep(1)
        forward.release()
        

forward, backward = Semaphore(1), Semaphore(0)
workers = [
    Thread(target=ping, args=(forward, backward)),
    Thread(target=pong, args=(forward, backward))
]
for worker in workers:
    worker.start()
