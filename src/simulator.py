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
running_process = None

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


def running():
    global running_process
    while True:
        for queue in [Queue1, Queue2, Queue3, Queue4]:
            if not queue.empty():
                process = queue.get()
                print("➡️\tProcess ", process.id, " is running")
                running_process = process
                sleep(process.brusts[0])
                running_process = None
                if len(process.brusts) == 1:
                    print("✅\tProcess ", process.id, " is finished")
                else:
                    process.rank += 1
                    process.brusts.pop(0)
                    process.arrival_time = global_timer + 1
                    Waiting.append(process)
                break


def waiting():
    while True:
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
    print("💤\t Process ", process.id, " is waiting for ", time, " seconds")
    sleep(time)
    process.brusts.pop(0)
    process.arrival_time = global_timer + 1
    Waiting.remove(process)
    process.waiting = False
    ready_processes.append(process)


def debug():
    global global_waiting
    while True:
        print("===============================================================",
              "Time: ", global_timer)
        sleep(970/1000)
        print("\tWaiting: ", ", ".join([str(x.id) for x in Waiting]))
        print("\tProcesses: ", ", ".join(str(x.id) for x in ready_processes))
        print("\tRunning: ", running_process.id if running_process else "None")
        print("\tQueue1: ", ", ".join([str(x.id) for x in list(
            Queue1.queue)]))
        print("\tQueue2: ", ", ".join([str(x.id) for x in list(
            Queue2.queue)]))
        print("\tQueue3: ", ", ".join([str(x.id) for x in list(
            Queue3.queue)]))
        print("\tQueue4: ", ", ".join([str(x.id) for x in list(
            Queue4.queue)]))
        sleep(3/1000)


if __name__ == "__main__":
    ready_processes=read_processes("processes.txt")
    Thread(target=enque).start()
    Thread(target=debug).start()
    Thread(target=waiting).start()
    Thread(target=running).start()
