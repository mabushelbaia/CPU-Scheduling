from queue import Queue
from threading import Thread, Event
from time import sleep
from workload import Process, read_processes

Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Waiting = []
Finished = []
global_timer = 0
running_process = None


def clock():
    global global_timer
    while True:
        print("Clock: Ticking...")
        sleep(1)
        # Send signal to other threads
        for t in threads:
            t.event.set()
        global_timer += 1


def enqueue():
    global global_timer
    while True:
        event.wait()
        for process in processes:
            if process.arrival_time == global_timer:
                Queue1.put(process)
                print(
                    "📥\t\tProcess ", process.id, " is enqueued at time ", global_timer
                )
        event.clear()


if __name__ == "__main__":
    processes = read_processes("processes.txt")
    threads = []
    event = Event()
    t = Thread(target=enqueue)
    t.event = event
    threads.append(t)
    t.start()
    control_thread = Thread(target=clock)
    control_thread.start()
