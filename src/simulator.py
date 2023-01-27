from queue import Queue
from threading import Thread
from time import sleep
from workload import Process, read_processes
Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Waiting = []
ready_queue = Queue()
global_timer = 0
global_waiting = 0


def enque():
    global global_timer
    queues = [Queue1, Queue2, Queue3, Queue4]
    while True:
        print("===============================================================",
              "Time: ", global_timer)
        for process in ready_processes:
            if process.arrival_time == global_timer:
                queues[process.rank - 1].put(process)
                ready_processes.remove(process)
        global_timer += 1
        sleep(1)


def waiting():
    global global_waiting
    while True:
        if len(Waiting):
            for process in Waiting:
                global_waiting += 1
                Thread(target=sleep_thread, args=(
                    process.brusts[0], process)).start()
                Waiting.remove(process)
        sleep(1)


def sleep_thread(time: int, process: Process):
    global global_timer, global_waiting
    print("Process ", process.id, " is waiting for ", time, " seconds")
    sleep(time)
    process.brusts.pop(0)
    process.arrival_time = global_timer + 1
    global_waiting -= 1
    ready_processes.append(process)


def debug():
    global global_waiting
    while True:
        print("Queue1: ", Queue1.qsize())
        print("Queue2: ", Queue2.qsize())
        print("Queue3: ", Queue3.qsize())
        print("Queue4: ", Queue4.qsize())
        print("Waiting: ", global_waiting)
        print("Processes: ", len(ready_processes))
        sleep(1)


if __name__ == "__main__":
    ready_processes = read_processes("processes.txt")
    Thread(target=enque).start()
    Thread(target=debug).start()
    Thread(target=waiting).start()
