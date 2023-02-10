from queue import Queue
from threading import Thread, Semaphore, Lock
from time import sleep
from typing import List
from workload import Process, read_processes
from copy import deepcopy
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
no_intterupts = True
flags = [True, True, True, True]


def enque():
    global global_timer
    while True:
        if stop_threads:
            return
        for process in processes:
            if process.arrival_time == global_timer:
                Queue1.put(process)
                print("📥\t\tProcess ", process.id,
                      " is enqueued at time ", global_timer)
        sleep(1)


def running():
    global running_process, global_timer
    threads = [None, None, None, None]
    while True:
        if stop_threads:
            return
        if not Queue1.empty():
            if flags[0]:
                flags[0] = False
                threads[0] = Thread(
                    target=round_robin, args=(Queue1, q1, 1)).start()
        elif not Queue2.empty():
            if flags[1]:
                flags[1] = False
                if threads[0]:
                    threads[0].join()
                Thread(target=round_robin, args=(Queue2, q2, 2)).start()
        global_timer += 1
        sleep(1)


def round_robin(queue: Queue, time_quantum: int, rank: int):
    global running_process, global_timer, flags
    while not queue.empty():
        if flags[0] == False and rank == 2:
            flags[1] = True
            return
        process = queue.get()
        running_process = process
        time = 0
        while time < time_quantum:
            if time == 0:
                print("⚙️\t\tProcess ", process.id,
                      " is running from time ", global_timer)
            process.brusts[0] -= 1
            if process.brusts[0] == 0:
                if len(process.brusts) == 1:
                    process.brusts.pop(0)
                    print("✅\t\tProcess ", process.id,
                          " is finished at time ", global_timer)
                    running_process = None
                    Finished.append(process)
                else:
                    process.brusts.pop(0)
                    Waiting.append(process)
                    running_process = None
                break
            time += 1
            sleep(1)
        else:
            queue.put(process)
            process.counter += 1
            if process.counter == 10:
                process.rank += 1
                print("⬆️\t\tProcess ", process.id,
                      " is demoted to rank ", process.rank)
                process.counter = 0
    if rank == 1:
        flags[0] = True
    elif rank == 2:
        flags[1] = True
    return


def waiting():
    while True:
        if stop_threads:
            return
        if len(Waiting):
            for process in Waiting:
                if process.waiting:
                    continue
                Thread(target=sleep_thread, args=(
                    process.brusts[0], process)).start()
                process.waiting = True
        sleep(1)


def sleep_thread(time: int, process: Process):
    global global_timer
    print("⌛\t\tProcess ", process.id, " is waiting for ",
          time, " seconds at time ", global_timer)
    sleep(time)
    process.brusts.pop(0)
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
    Thread(target=running).start()
    Thread(target=enque).start()
    Thread(target=waiting).start()
    Thread(target=finish).start()


"""
def FCFS(queue: Queue):
    global running_process, global_timer
    while queue.empty() == False:
        process = queue.get()
        running_process = process
        time = 0
        while time < process.brusts[0]:
            lock.acquire()
            if time == 0:
                print("⚙️\t\tProcess ", process.id,
              " is running from time ", global_timer)
            process.brusts[0] -= 1
            if process.brusts[0] == 0:
                if len(process.brusts) == 1:
                    process.brusts.pop(0)
                    print("✅\t\tProcess ", process.id,
                          " is finished at time ", global_timer)
                    running_process = None
                    Finished.append(process)
                else:
                    process.brusts.pop(0)
                    Waiting.append(process)
                    running_process = None
            time += 1
            lock.release()
            sleep(1)
"""
