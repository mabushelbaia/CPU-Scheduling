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
    global global_timer, running_process, num_processes
    while True:
        print("============================================")
        to_remove = []
        to_append = None
        for process in processes:
            if process.arrival_time == global_timer:
                if process.status == "Waiting":
                    print("⏳\t\tProcess ", process.id, " started waiting at time ", global_timer, "for ", process.bursts[0], "ms")
                    running_process = None
                    Waiting.append(process)
                elif process.status == "Finished":
                    print("🏁\t\tProcess ", process.id, " Finished at time ", global_timer, "ms")
                    running_process = None
                    Finished.append(process)
                elif process.status == "Running": # Preempted process
                    running_process = None
                    process.status = "Ready"
                    to_append = process
                else:                           # New process or finished waiting
                    Queues[process.rank - 1].put(process)
                    if process in Waiting:
                        Waiting.remove(process)
                    print("📥\t\tProcess ", process.id, " is enqueued at time ", global_timer, "ms")
                to_remove.append(process)
        if to_append is not None:
            if to_append.rank == 1  and to_append.counter == 3:
                to_append.rank = 2
                to_append.counter = 0
                print("🔽\t\tProcess ", process.id, " is demoted to rank ", process.rank, " at time ", global_timer, "ms")
                print("📥\t\tProcess ", process.id, " is enqueued at time ", global_timer, "ms")
            Queues[to_append.rank - 1].put(to_append)
            to_append = None
        if running_process is not None:
            if not Queue1.empty():
                if running_process.rank > 1:
                    Queues[running_process.rank - 1].put(running_process)
                    running_process.status = "Ready"
                    running_process = Queue1.get()
                    running_process.status = "Running"
                    running_process.quantum = 10
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")

            elif  not Queue2.empty():
                if running_process.rank > 2:
                    Queues[running_process.rank - 1].put(running_process)
                    running_process.status = "Ready"
                    running_process = Queue2.get()
                    running_process.status = "Running"
                    running_process.quantum = 5
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
        else:
            if not Queue1.empty():
                running_process = Queue1.get()
                running_process.status = "Running"
                running_process.quantum = 10
                print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
            elif not Queue2.empty():
                running_process = Queue2.get()
                running_process.status = "Running"
                running_process.quantum = 5
                print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
        
        for process in to_remove:
            processes.remove(process)
        for t in threads:
            t.event.set()
        for t in threads:
            t.event.clear()
        sleep(0.01)
        print("Time:  ", global_timer)
        print("Queue 1: ", [x.id for x in list(Queue1.queue)])
        print("Queue 2: ", [x.id for x in list(Queue2.queue)])
        print("Waiting: ", [x.id for x in Waiting])
        print("Running: ", running_process.id if running_process else None)
        print("Finished: ", [x.id for x in Finished])
        if len(Finished) == num_processes:
            global_timer = -1
            return
        global_timer += 1


def waiting():
    global global_timer
    while True:
        if global_timer == -1:
            return
        event.wait()
        for process in Waiting:
            if process.bursts[0] == 1:
                process.bursts.pop(0)
                process.status = "Ready"
                process.arrival_time = global_timer + 1
                processes.append(process)
            else:
                process.bursts[0] -= 1
        
def running():
    global global_timer, running_process
    while True:
        if global_timer == -1:
            return
        event.wait()
        if running_process is not None:
            if running_process.rank == 1 or running_process.rank == 2:
                running_process.bursts[0] -= 1
                running_process.quantum -= 1
            if running_process.quantum == 0 or running_process.bursts[0] == 0:
                running_process.counter += 1
                if running_process.bursts[0] == 0:
                    if len(running_process.bursts) == 1:
                        running_process.status = "Finished"
                        running_process.bursts.pop(0)
                        running_process.arrival_time = global_timer + 1
                        processes.append(running_process)
                    else:
                        running_process.bursts.pop(0)
                        running_process.status = "Waiting"
                        running_process.arrival_time = global_timer + 1
                        processes.append(running_process)
                else:
                    running_process.arrival_time = global_timer + 1
                    processes.append(running_process)

if __name__ == "__main__":
    processes = read_processes("processes.txt")
    num_processes = len(processes)
    global_timer = 0
    running_process = None
    threads = []
    targets = [waiting, running,]
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    Thread(target=clock).start()