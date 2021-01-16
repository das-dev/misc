from threading import Thread, Semaphore


def thread_A(mutex):
    global count

    mutex.acquire()
    count = count + 1
    print(count)
    mutex.release()


def thread_B(mutex):
    global count

    mutex.acquire()
    count = count + 1
    print(count)
    mutex.release()


count = 0
mutex = Semaphore()
workers = [
    Thread(target=thread_A, args=(mutex,)),
    Thread(target=thread_B, args=(mutex,))
]

for worker in workers:
    worker.start()

for worker in workers:
    worker.join()

