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
running_process: Process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]
time_quantum_1 = int(input("Enter the time quantum for queue 1: "))
time_quantum_2 = int(input("Enter the time quantum for queue 2: "))

waiting_lock = Lock()
finished_lock = Lock()
running_lock = Lock()


def clock():
    global global_timer
    while True:
        # Send signal to other threads
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
                with waiting_lock:
                    Waiting.append(process)
                print(
                    "📥\t\tProcess ", process.id, " is enqueued at time ", global_timer
                )


def running():
    while True:
        if not Queue1.empty:
            running_process = Queue1.get()
            counter = 0
            while counter < time_quantum_1 and running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                running_process.counter += 1
                counter += 1
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if running_process.counter == 10*time_quantum_1:
                    running_process.rank += 1
                    running_process.counter = 0
                    Queue2.put(running_process)
                    break
                if running_process.bursts[0] > 0 and counter == time_quantum_1:
                    Queue1.put(running_process)
                    break
        elif Queue1.empty() and not Queue2.empty():
            running_process = Queue2.get()
            counter = 0
            while counter < time_quantum_2 and running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                running_process.counter += 1
                counter += 1
                if not Queue1.empty():
                    Queue2.put(running_process)
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if running_process.counter == 10*time_quantum_2:
                    running_process.rank += 1
                    Queue3.put(running_process)
                    break
                if running_process.bursts[0] > 0 and counter == time_quantum_2:
                    Queue2.put(running_process)
                    break


def waiting():
    global global_timer
    while True:
        event.wait()
        with waiting_lock:
            for process in Waiting:
                process.waiting_time += 1
                process.IO_time -= 1
                if process.IO_time == 0:
                    Waiting.remove(process)
                    process.remaining_time = 5
                    Queues[process.rank - 1].put(process)
                    print(
                        "📥\t\tProcess ",
                        process.id,
                        " is enqueued at time ",
                        global_timer + 1,
                        " after waiting for ", process.temp,
                    )


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
