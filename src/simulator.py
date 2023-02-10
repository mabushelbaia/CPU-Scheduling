from queue import Queue
from threading import Thread, Event, Lock
from time import sleep
from workload import Process
import os

Queue1: list[Process] = []
Queue2: list[Process] = []
Queue3: list[Process] = []
Queue4: list[Process] = []
Queues = [Queue1, Queue2, Queue3, Queue4]
Waiting = []
Finished = []
global_timer = 0
running_process: Process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]



processes: list[Process] = []
time_quantum_1 = 2
time_quantum_2 = 4
alpha = 0.5
processes_count = 0


def read_processes(filename: str) -> list[Process]:
    global processes_count
    with open(filename) as f:
        for line in f:
            process = line.split()
            processes.append(Process(int(process[0]), int(process[1]), [
                             int(burst) for burst in process[2:]]))
    processes_count = len(processes)
    print(processes_count)
    processes.sort(key=lambda process: process.arrival_time)
    for process in processes:
        print(process)




def enqueue():
    global global_timer
    while True:
        for process in processes:
            if process.arrival_time == global_timer:
                Queue1.append(process)
                processes.remove(process)
                print("\n📥 Process ", process.id,
                      " arrived at time ", global_timer, "\n")
        sleep(1*.000001)
        if len(processes) == 0:
            return



def increment_waiting():
    for process in Queue1:
        process.waiting_time += 1
    for process in Queue2:
        process.waiting_time += 1
    for process in Queue3:
        process.waiting_time += 1
    for process in Queue4:
        process.waiting_time += 1
    return


def IO():
    for process in Waiting:
        process.bursts[0] -= 1
        if process.bursts[0] == 0:
            process.bursts.pop(0)
            if process.rank == 1:
                Queue1.append(process)
            elif process.rank == 2:
                Queue2.append(process)
            elif process.rank == 3:
                process.predicted_time = (alpha * process.bursts[0])+((1-alpha)*process.predicted_time)
                Queue3.append(process)
            elif process.rank == 4:
                Queue4.append(process)
            Waiting.remove(process)



def running():
    global global_timer
    while True:
        print(len(Queue1), len(Queue2), len(Queue3), len(Queue4))
        if len(Queue1) > 0:
            running_process = Queue1.pop(0)
            counter = 0
            while (
                counter < time_quantum_1
                and running_process.bursts[0] > 0
                and len(running_process.bursts) > 0
            ):
                running_process.bursts[0] -= 1
                print("\n💡 Process ", running_process.id,
                      " is running at time ", global_timer, "in queue 1\n")
                sleep(1*.001)
                global_timer += 1
                IO()
                increment_waiting()
                running_process.counter += 1
                counter += 1
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to waiting queue\n")
                        break
                    else:
                        Finished.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to finished queue\n")
                        break
                if running_process.counter == 10 * time_quantum_1:
                    running_process.rank += 1
                    running_process.counter = 0
                    Queue2.append(running_process)
                    print("\n📤Process ", running_process.id,
                          " is enqueued at time ", global_timer, " to queue 2\n")
                    break
                if running_process.bursts[0] > 0 and counter == time_quantum_1:
                    Queue1.append(running_process)
                    print("\n📤Process ", running_process.id, " finished its time quantum at time ",
                          global_timer, " and is enqueued to queue 1\n")
                    break

        elif len(Queue1) == 0 and len(Queue2) > 0:
            running_process = Queue2.pop(0)
            counter = 0
            while (
                counter < time_quantum_2
                and running_process.bursts[0] > 0
                and len(running_process.bursts) > 0
            ):
                running_process.bursts[0] -= 1
                print("\n💡 Process ", running_process.id,
                      " is running at time ", global_timer, "in queue 2\n")
                sleep(1*.001)
                global_timer += 1
                IO()
                increment_waiting()
                running_process.counter += 1
                counter += 1
                if len(Queue1) > 0:
                    Queue2.append(running_process)
                    print("\n📤Process ", running_process.id, " has been preempted at time ",
                          global_timer, " to queue 2 by a process in queue 1\n")
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to waiting queue\n")
                        break
                    else:
                        Finished.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to finished queue\n")
                        break

                if running_process.counter == 10 * time_quantum_2:
                    running_process.rank += 1
                    running_process.predicted_time = (
                        alpha * running_process.bursts[0]
                    ) + ((1 - alpha) * running_process.predicted_time)
                    running_process.counter = 0
                    Queue3.append(running_process)
                    print("\n📤Process ", running_process.id,
                          " is enqueued at time ", global_timer, " to queue 3\n")
                    break
                if running_process.bursts[0] > 0 and counter == time_quantum_2:
                    Queue2.append(running_process)
                    print("\n📤Process ", running_process.id, " finished its time quantum at time ",
                          global_timer, " and is enqueued to queue 2\n")
                    break

        elif len(Queue1) == 0 and len(Queue2) == 0 and len(Queue3) > 0:
            # Sort the queue based on the predicted time
            Queue3.sort(key=lambda x: x.predicted_time)
            running_process = Queue3.pop(0)

            while running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                
                print("\n💡 Process ", running_process.id,
                      " is running at time ", global_timer, "in queue 3\n")
                sleep(1*.001)
                global_timer += 1
                IO()
                increment_waiting()
                if len(Queue1) > 0 or len(Queue2) > 0:
                    Queue3.append(running_process)
                    print("\n📤Process ", running_process.id, " has been preempted at time ",
                          global_timer, " to queue 3 by a process in queue 1 or 2\n")
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to waiting queue\n")
                        break
                    else:
                        Finished.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to finished queue\n")
                        break
                if len(Queue3) > 0:
                    Queue3.sort(key=lambda x: x.predicted_time)
                    if running_process.predicted_time > Queue3[0].predicted_time:
                        running_process.counter += 1
                        if running_process.counter == 3:
                            running_process.rank += 1
                            running_process.counter = 0
                            Queue4.append(running_process)
                            print("\n📤Process ", running_process.id,
                                  " is enqueued at time ", global_timer, " to queue 4\n")
                            break
                        else:
                            Queue3.append(running_process)
                            print("\n📤Process ", running_process.id, " has been preempted at time ",
                                  global_timer, " to queue 3 by a process in queue 3\n")
                            break
        elif (
            len(Queue1) == 0
            and len(Queue2) == 0
            and len(Queue3) == 0
            and len(Queue4) > 0
        ):
            running_process = Queue4.pop(0)

            while running_process.bursts[0] > 0 and len(running_process.bursts) > 0:
                running_process.bursts[0] -= 1
                sleep(1*.001)
                global_timer += 1
                print("\n💡 Process ", running_process.id,
                      " is running at time ", global_timer, "in queue 4\n")
                IO()
                increment_waiting()
                if len(Queue1) > 0 or len(Queue2) > 0 or len(Queue3) > 0:
                    Queue4.append(running_process)
                    print("\n📤Process ", running_process.id, " has been preempted at time ",
                          global_timer, " to queue 4 by a process in queue 1, 2 or 3\n")
                    break
                if running_process.bursts[0] == 0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts) > 0:
                        Waiting.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to waiting queue\n")
                        break
                    else:
                        Finished.append(running_process)
                        print("\n📤Process ", running_process.id,
                              " is enqueued at time ", global_timer, " to finished queue\n")
                        break
                
        if len(Finished) == 6:
            for process in Finished:
                print("Process ", process.id, " finished")
            return
        elif len(Queue1) == 0 and len(Queue2) == 0 and len(Queue3) == 0 and len(Queue4) == 0 and len(Waiting) > 0:
            IO()
            global_timer += 1
            sleep(1*.001)
            continue
        sleep(1*.001)
        global_timer += 1
        
        


if __name__ == "__main__":
    read_processes("processes.txt")
    t1 = Thread(target=running)
    t2 = Thread(target=enqueue)
    t1.start()
    t2.start()
