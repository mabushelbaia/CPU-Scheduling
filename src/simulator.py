from queue import Queue
from threading import Thread, Event, Lock
from time import sleep
from workload import Process, read_processes

Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Queues = [Queue1, Queue2, Queue3, Queue4]
Waiting = []
Finished = []
global_timer = 0
running_process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]
Lock = Lock()

def clock():
    global global_timer
    while True:
        # Send signal to other threads
        print("Time  ", global_timer, ":")
        for t in threads:
            t.event.set()
            
        for t in threads:
            t.event.clear()
        sleep(1)
        global_timer += 1


def enqueue():
    global global_timer
    while True:
        event.wait()
        for process in processes:
            if process.arrival_time == global_timer:
                process.IO_time = 3
                process.temp = 3
                Waiting.append(process)
                print(
                    "📥\t\tProcess ", process.id, " is enqueued at time ", global_timer
                )

def waiting():
    global global_timer
    while True:
        event.wait()
        for process in Waiting:
            process.waiting_time += 1
            process.IO_time -= 1
            if process.IO_time == 0:
                Waiting.remove(process)
                process.remaining_time = 5
                Queues[process.rank - 1].put(process)

def running():
    global running_process, global_timer
    while True:
        event.wait()
        if not running_process:
            if not Queue1.empty():
                running_process = Queue1.get()
                print(
                    "📥\t\tProcess ",
                    running_process.id,
                    " is running at time ",
                    global_timer,
                )
        else:
            running_process.execution_time += 1
            running_process.remaining_time -= 1
            if running_process.remaining_time == 1:
                Finished.append(running_process)
                running_process = None

if __name__ == "__main__":
    processes = read_processes("processes.txt")
    threads = []
    targets = [enqueue, waiting, running]
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    control_thread = Thread(target=clock)
    control_thread.start()