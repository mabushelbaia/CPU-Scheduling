from queue import Queue
from threading import Thread
from time import sleep
from workload import Process, read_processes
Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Waiting = []
global_timer = 0
global_waiting = 0


def enque():
    global global_timer
    queues = [Queue1, Queue2, Queue3, Queue4]
    while True:
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
        print("===============================================================",
              "Time: ", global_timer)
        sleep(970/1000)
        a, b, c, d = "Empty", "Empty", "Empty", "Empty"
        for queue in [Queue1, Queue2, Queue3, Queue4]:
            if queue.empty():
                ["Empty"]
            else:
                list(queue.queue)
        print("Queue1: ", ", ".join([str(x.id) for x in list(
            Queue1.queue)] if not Queue1.empty() else ["Empty"]))
        print("Queue2: ", ", ".join([str(x.id) for x in list(
            Queue2.queue)] if not Queue2.empty() else ["Empty"]))
        print("Queue3: ", ", ".join([str(x.id) for x in list(
            Queue3.queue)] if not Queue3.empty() else ["Empty"]))
        print("Queue4: ", ", ".join([str(x.id) for x in list(
            Queue4.queue)] if not Queue4.empty() else ["Empty"]))
        print("Waiting: ", global_waiting)
        print("Ready: ", ", ".join(str(x.id) for x in ready_processes))
        sleep(3/1000)


if __name__ == "__main__":
    ready_processes = read_processes("processes.txt")
    Thread(target=debug).start()
    Thread(target=enque).start()
    Thread(target=waiting).start()
