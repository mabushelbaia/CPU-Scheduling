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
global_waiting = 0
running_process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]

def clock():
    global global_timer
    while True:
        sleep(1)
        # Send signal to other threads
        for t in threads:
            t.event.set()
        # Reset event for next iteration
        for t in threads:
            t.event.clear()
        global_timer += 1
        

def enqueue():
    global global_timer
    while True:
        if stop_threads:
            return
        event.wait()
        for process in processes:
            if process.arrival_time == global_timer:
                Queue1.put(process)
                print("📥\t\tProcess ", process.id,
                      " is enqueued at time ", global_timer)


def waiting():
    while True:
        if stop_threads:
            return
        if len(Waiting):
            for process in Waiting:
                if process.waiting:
                    continue
                Thread(target=sleep_thread, args=(
                    process.bursts[0], process)).start()
                process.waiting = True
        sleep(1)


def sleep_thread(time: int, process: Process):
    global global_timer
    print("⌛\t\tProcess ", process.id, " is waiting for ",
          time, " seconds at time ", global_timer)
    sleep(time)
    process.bursts.pop(0)
    Waiting.remove(process)
    process.waiting = False
    [Queue1, Queue2, Queue3, Queue4][process.rank - 1].put(process)


def finish():
    global stop_threads
    while True:
        if len(Finished) == len(processes):
            stop_threads = True
            print("😁\t\tAll processes are finished at time ", global_timer)
            return


if __name__ == "__main__":
    processes = read_processes("processes.txt")
    q1, q2 = map(int, input(
        "Enter time quantum for queue 1 and queue 2: ").split())
    alpha = float(input("Enter alpha: "))
    # Create a list to store the threads
    threads = []
    event = Event()
    t = Thread(target=enqueue)
    t.event = event
    threads.append(t)
    t.start()