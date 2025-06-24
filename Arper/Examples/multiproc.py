from multiprocessing import Process
import os

def worker_process(name):
    print(f'Hello {name}, this is process with ID: {os.getpid()}')

if __name__ == "__main__":
    print(f'This is main process have ID: {os.getpid()}')

    process = Process(target=worker_process, args=('World',))

    process.start()

    process.join() #Waiting

    print('process close')



