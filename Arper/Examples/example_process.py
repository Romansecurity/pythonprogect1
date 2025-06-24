from multiprocessing import Process
import os

def work_process(name):
    print(f'Hello {name}, this is process {os.getpid()}')

if __name__ == '__main__':
    print(f'This is main process have ID:{os.getpid()}')

    process = Process(target=work_process, args=('world',))

    process.start()

    process.join()

    process.close()
    print('process close')