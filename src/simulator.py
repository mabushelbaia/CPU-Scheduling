from queue import Queue
from threading import Thread, Event, Lock
from time import sleep
from workload import Process, read_processes
import sys

Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Queues = [Queue1, Queue2, Queue3, Queue4]
Waiting = []
Finished = []


def clock():
    global global_timer, running_process, running_lock, next_message, num_processes
    while True:
        print("============================================")
        to_remove = []
        for process in processes:
            if process.arrival_time == global_timer:
                if process.waiting:
                    print("⏳\t\tProcess ", process.id, " started waiting at time ", global_timer, "for ", process.bursts[0], "ms")
                    Waiting.append(process)
                elif process.finished:
                    print("🏁\t\tProcess ", process.id, " Finished at time ", global_timer, "ms")
                    Finished.append(process)
                else:
                    Queues[process.rank - 1].put(process)
                    if process in Waiting:
                        Waiting.remove(process)
                    print("📥\t\tProcess ", process.id, " is enqueued at time ", global_timer, "ms")
                to_remove.append(process)
        for process in to_remove:
            processes.remove(process)
        for message in next_message:
            print(message, global_timer)
            next_message.remove(message)
        for t in threads:
            t.event.set()
            t.event.clear()
        sleep(2)
        print("Time:  ", global_timer)
        print("Queue 1: ", [x.id for x in list(Queue1.queue)])
        print("Waiting: ", [x.id for x in Waiting])
        print("Running: ", running_process.id if running_lock and running_process else None)
        print("Finished: ", [x.id for x in Finished])
        if len(Finished) == num_processes:
            sys.exit(0)
        global_timer += 1


def waiting():
    global running_process, running_lock, global_timer, next_message
    while True:
        event.wait()
        for process in Waiting:
            if process.bursts[0] == 1:
                process.bursts.pop(0)
                process.waiting = False
                process.arrival_time = global_timer + 1
                processes.append(process)
            else:
                process.bursts[0] -= 1
            sleep(1)
def running():
    global running_process, running_lock, global_timer, next_message
    while True:
        event.wait()
        if running_lock is True:
            running_process.bursts[0] -= 1
            if running_process.bursts[0] == 1:
                if len(running_process.bursts) == 1:
                    running_process.finished = True
                    running_process.bursts.pop(0)
                    running_process.arrival_time = global_timer + 1
                    processes.append(running_process)
                    running_lock = False
                else:
                    running_process.bursts.pop(0)
                    running_process.waiting = True
                    running_process.arrival_time = global_timer + 1
                    processes.append(running_process)
                    running_lock = False
        else:
            running_process = Queue1.get()
            if running_process is not None:
                print("⚙️\t\tProcess ", running_process.id, " started running at time ", global_timer, "ms", "for ", running_process.bursts[0], "ms") 
                running_lock = True
            sleep(1)

if __name__ == "__main__":
    processes = read_processes("processes.txt")
    num_processes = len(processes)
    global_timer = 0
    running_process = None
    next_message = []
    running_lock = False
    threads = []
    targets = [waiting, running]
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    Thread(target=clock).start()
    
