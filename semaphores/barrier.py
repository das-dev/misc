import time
from threading import Thread, Semaphore


THREADS_NUMBER = 2


def rendezvous(mutex, barrier):
    global count
    
    mutex.acquire()
    count += 1
    mutex.release()

    if count != THREADS_NUMBER:
        barrier.acquire()
    barrier.release()


def critical_section(thread_number):
    print(f'critical section {thread_number} perform')
    time.sleep(1)


def thread(thread_number, mutex, barrier):
    print(f'non-critical section {thread_number} perform')
    rendezvous(mutex, barrier)
    critical_section(thread_number)


count = 0
mutex = Semaphore(THREADS_NUMBER - 1)
barrier = Semaphore(0)
workers = [
    Thread(target=thread, args=(n, mutex, barrier))
    for n in range(THREADS_NUMBER)
]
for worker in workers:
    worker.start()
for worker in workers:
    worker.join()

