from queue import Queue
from threading import Thread, Event, Lock
from time import sleep
from workload import Process, read_processes

Queue1 = Queue()
Queue2 = Queue()
Queue3: list[Process] = []
Queue4 = Queue()
Queues = [Queue1, Queue2, Queue3, Queue4]
Waiting = []
Finished = []
global_timer = 0
running_process: Process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]


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
                Queue1.put(process)
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
    while True:
        event.wait()
        if not Queue1.empty:
            running_process = Queue1.get()
            counter = 0
            while (
                counter < time_quantum_1
                and running_process.bursts[0] > 0
                and len(running_process.bursts) > 0
            ):
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
                if running_process.counter == 10 * time_quantum_1:
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
            while (
                counter < time_quantum_2
                and running_process.bursts[0] > 0
                and len(running_process.bursts) > 0
            ):
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
                if running_process.counter == 10 * time_quantum_2:
                    running_process.rank += 1
                    running_process.predicted_time = (
                        alpha * running_process.bursts[0]
                    ) + ((1 - alpha) * running_process.predicted_time)
                    running_process.counter = 0
                    Queue3.put(running_process)
                    break
                if running_process.bursts[0] > 0 and counter == time_quantum_2:
                    Queue2.put(running_process)
                    break
        elif Queue1.empty() and Queue2.empty() and len(Queue3) > 0:
            # Sort the queue based on the predicted time
            Queue3.sort(key=lambda x: x.predicted_time)
            running_process = Queue3.pop(0)
            while running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                if not Queue1.empty() or not Queue2.empty():
                    Queue3.append(running_process)
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if len(Queue3) > 0:
                    if (
                        Queue3.sort(key=lambda x: x.predicted_time)[0].predicted_time
                        < running_process.predicted_time
                    ):
                        running_process.counter += 1
                        if running_process.counter == 3:
                            running_process.rank += 1
                            running_process.counter = 0
                            Queue4.put(running_process)
                            break
                        else:
                            Queue3.append(running_process)
                            break
                if running_process.bursts[0] > 0:
                    Queue3.append(running_process)
                    break
        elif (
            Queue1.empty()
            and Queue2.empty()
            and len(Queue3) == 0
            and not Queue4.empty()
        ):
            running_process = Queue4.get()
            while running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                if not Queue1.empty() or not Queue2.empty() or len(Queue3) > 0:
                    Queue4.put(running_process)
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if running_process.bursts[0] > 0:
                    Queue4.put(running_process)
                    break


if __name__ == "__main__":
    processes = read_processes("processes.txt")
    time_quantum_1 = 2
    time_quantum_2 = 4
    alpha=0.5
    threads = []
    targets = [enqueue,  running]
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    control_thread = Thread(target=clock)
    control_thread.start()
