from threading import Thread, Semaphore


CONCURRENT_THREADS = 2

def thread(mutex):
    global count

    mutex.acquire()
    count = count + 1
    print(count)
    mutex.release()


count = 0
mutex = Semaphore(CONCURRENT_THREADS)
workers = [
    Thread(target=thread, args=(mutex,)),
    Thread(target=thread, args=(mutex,)),
    Thread(target=thread, args=(mutex,))
]

for worker in workers:
    worker.start()

for worker in workers:
    worker.join()

