import os
from time import sleep
from threading import Thread, Lock
from copy import deepcopy
import queue
from Workload_Generator import Process, max_time, processes_count
from prettytable import *
time = 0 # time counter
time_scale = .00001
arrival_timeline = [x*time_scale for x in range(max_time+1)]


time_quantum_1 = 4
time_quantum_2 = 8
alpha = 0.5


processes: list[Process] = []


ready_queue_1 = queue.Queue()
ready_queue_2 = queue.Queue()
ready_queue_3: list[Process] = []
ready_queue_4 = queue.Queue()

waiting_queue_1: list[Process] = []
waiting_queue_2: list[Process] = []
waiting_queue_3: list[Process] = []
waiting_queue_4: list[Process] = []

finished_queue: list[Process] = []

running = []


def read_processes():
    with open("processes.txt", "r") as file:
        for line in file:
            line = line.strip()
            parts = line.split(" ")
            
            id = int(parts[0])
            arrival_time = int(parts[1])
            bursts = [int(burst) for burst in parts[2:]]
            processes.append(Process(id, arrival_time, bursts))
        processes.sort(key=lambda process: process.arrival_time)

def enqueue():
    timer = 0
    while True:
        for i in arrival_timeline:
            for process in processes:
                if process.arrival_time*time_scale == i:
                    ready_queue_1.put(process)
                    print(f"process {process.id} is added to ready queue 1 at time {i/time_scale}\n")
            sleep(1*time_scale)
            timer += 1
        return


def increment_waiting_time():
    # increment waiting time for all processes in all ready queues
    for process in ready_queue_1.queue:
        process.waiting_time += 1
        
    for process in ready_queue_2.queue:
        process.waiting_time += 1
        
    for process in ready_queue_3:
        process.waiting_time += 1
        
    for process in ready_queue_4.queue:
        process.waiting_time += 1
    return


def IO(process: Process):
    print(f"process {process.id} is in IO\n")
    for _ in range(process.bursts[0]):
        sleep(1*time_scale)
    if process.queue == 1:
        process.bursts.pop(0)
        ready_queue_1.put(process)
        print(f"process {process.id} is added to ready queue 1 after the IO\n")
    if process.queue == 2:
        process.bursts.pop(0)
        ready_queue_2.put(process)
        print(f"process {process.id} is added to ready queue 2 after the IO\n")
    if process.queue == 3:
        process.bursts.pop(0)
        predicated_time = (
            process.bursts[0]*alpha)+(process.predicted_time*(1-alpha))
        process.predicted_time = predicated_time
        ready_queue_3.append(process)
        print(f"process {process.id} is added to ready queue 3 after the IO\n")
    if process.queue == 4:
        process.bursts.pop(0)
        ready_queue_4.put(process)
        print(f"process {process.id} is added to ready queue 4 after the IO\n")
    return


def check_all_waiting_queues():
    while True:
        while len(waiting_queue_1) > 0:
            process = waiting_queue_1.pop(0)
            Thread(target=IO, args=(process,)).start()
        while len(waiting_queue_2) > 0:
            process = waiting_queue_2.pop(0)
            Thread(target=IO, args=(process,)).start()
        while len(waiting_queue_3) > 0:
            process = waiting_queue_3.pop(0)
            Thread(target=IO, args=(process,)).start()
        while len(waiting_queue_4) > 0:
            process = waiting_queue_4.pop(0)
            Thread(target=IO, args=(process,)).start()


def CPU():
    while True:
        if not ready_queue_1.empty() and len(running) == 0:
            process = ready_queue_1.get()
            running.append(process)
            print(f"process {process.id} is running\n")
            count = 0
            while count < time_quantum_1 and process.bursts[0] > 0 and len(process.bursts) >= 1:
                process.bursts[0] -= 1
                count += 1
                increment_waiting_time()
                sleep(1*time_scale)
                process.counter += 1
                if process.bursts[0] == 0 and len(process.bursts) > 1:
                    process.bursts.pop(0)
                    waiting_queue_1.append(process)
                    print(
                        f"process {process.id} is added to waiting queue 1\n")
                    break
                elif process.bursts[0] == 0 and len(process.bursts) == 1:
                    process.bursts.pop(0)
                    finished_queue.append(process)
                    print(f"process {process.id} is finished\n")
                    break

                if process.counter == 10*time_quantum_1:
                    process.queue = 2
                    process.counter = 0
                    ready_queue_2.put(process)
                    print(f"process {process.id} is added to ready queue 2\n")
                    break

                if count == time_quantum_1 and process.bursts[0] > 0:
                    ready_queue_1.put(process)
                    print(f"process {process.id} is added to ready queue 1\n")
                    break
            running.pop(0)
        if not ready_queue_2.empty() and ready_queue_1.empty() and len(running) == 0:
            process = ready_queue_2.get()
            running.append(process)
            print(f"process {process.id} is running\n")
            count = 0
            while count < time_quantum_2:
                process.bursts[0] -= 1
                count += 1
                increment_waiting_time()
                sleep(1*time_scale)
                process.counter += 1
                if not ready_queue_1.empty():
                    ready_queue_2.put(process)
                    print(
                        f"process {process.id} has been interrupted and added to ready queue 2\n")
                    break

                if process.bursts[0] == 0 and len(process.bursts) > 1:
                    process.bursts.pop(0)
                    waiting_queue_2.append(process)
                    print(
                        f"process {process.id} is added to waiting queue 2\n")
                    break
                if process.bursts[0] == 0 and len(process.bursts) == 1:
                    process.bursts.pop(0)
                    finished_queue.append(process)
                    print(f"process {process.id} is finished\n")
                    break

                if process.counter == 10*time_quantum_2:
                    process.queue = 3
                    process.counter = 0
                    predicted_time = alpha * \
                        process.bursts[0]+(1-alpha)*process.predicted_time
                    process.predicted_time = predicted_time
                    ready_queue_3.append(process)
                    print(f"process {process.id} is added to ready queue 3\n")
                    break

                if count == time_quantum_2 and process.bursts[0] > 0:
                    ready_queue_2.put(process)
                    print(f"process {process.id} is added to ready queue 2\n")
            running.pop(0)
        if len(ready_queue_3) > 0 and ready_queue_1.empty() and ready_queue_2.empty() and len(running) == 0:
            index = find_minimum_predicted_time()
            min = ready_queue_3[index].predicted_time
            process = ready_queue_3.pop(index)
            running.append(process)
            print(f"process {process.id} is running\n")
            while process.bursts[0] > 0 and len(process.bursts) >= 1:
                process.bursts[0] -= 1
                increment_waiting_time()
                sleep(1*time_scale)
                if not ready_queue_1.empty() or not ready_queue_2.empty():
                    process.counter += 1
                    ready_queue_3.append(process)
                    print(
                        f"process {process.id} has been interrupted and added to ready queue 3\n")

                    break
                else:
                    index2 = find_minimum_predicted_time()
                    if index2 == -1:
                        pass
                    elif min > ready_queue_3[index2].predicted_time:
                        ready_queue_3.append(process)
                        print(
                            f"process {process.id} has been interrupted by and added to ready queue 3\n")
                        break
                if process.bursts[0] == 0 and len(process.bursts) > 1:
                    process.bursts.pop(0)
                    waiting_queue_3.append(process)
                    print(
                        f"process {process.id} is added to waiting queue 3\n")
                    break
                if process.bursts[0] == 0 and len(process.bursts) == 1:
                    process.bursts.pop(0)
                    finished_queue.append(process)
                    print(f"process {process.id} is finished\n")
                    break
                if process.counter == 3:
                    process.queue = 4
                    process.counter = 0
                    ready_queue_4.put(process)
                    print(f"process {process.id} is added to ready queue 4\n")
                    break
            running.pop(0)

        if not ready_queue_4.empty() and ready_queue_1.empty() and ready_queue_2.empty() and len(ready_queue_3) == 0 and len(running) == 0:
            process = ready_queue_4.get()
            running.append(process)
            print(f"process {process.id} is running\n")
            while process.bursts[0] > 0 and len(process.bursts) >= 1:
                process.bursts[0] -= 1
                increment_waiting_time()
                sleep(1*time_scale)
                if not ready_queue_1.empty() or not ready_queue_2.empty() or len(ready_queue_3) != 0:
                    ready_queue_4.put(process)
                    print(
                        f"process {process.id} has been interrupted and added to ready queue 4\n")
                    break
                if process.bursts[0] == 0 and len(process.bursts) > 1:
                    process.bursts.pop(0)
                    waiting_queue_4.append(process)
                    print(
                        f"process {process.id} is added to waiting queue 4\n")
                    break
                elif process.bursts[0] == 0 and len(process.bursts) == 1:
                    process.bursts.pop(0)
                    finished_queue.append(process)
                    print(f"process {process.id} is finished\n")

                    break
            running.pop(0)


def find_minimum_predicted_time():
    if len(ready_queue_3) == 0:
        return -1
    min = ready_queue_3[0].predicted_time
    index = 0
    for i in range(len(ready_queue_3)):
        if ready_queue_3[i].predicted_time < min:
            min = ready_queue_3[i].predicted_time
            index = i
    return index


def debug():
    while True:
        with open("RR1.txt", "a") as file:
            print("ready queue 1", file=file)
            for process in ready_queue_1.queue:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("RR2.txt", "a") as file:
            print("ready queue 2", file=file)
            for process in ready_queue_2.queue:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("waiting_queue_1.txt", "a") as file:
            print("waiting queue 1", file=file)
            for process in waiting_queue_1:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("waiting_queue_2.txt", "a") as file:
            print("waiting queue 2", file=file)
            for process in waiting_queue_2:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("finished_queue.txt", "a") as file:
            print("finished queue", file=file)
            for process in finished_queue:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("running.txt", "a") as file:
            print("running", file=file)
            for process in running:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("SRTF.txt", "a") as file:
            print("SRTF", file=file)
            for process in ready_queue_3:
                print(process, file=file)
            print("------------------------------------------------", file=file)
        with open("FCFS.txt", "a") as file:
            print("FCFS", file=file)
            for process in ready_queue_4.queue:
                print(process, file=file)
            print("------------------------------------------------", file=file)


def end():
    while True:
        if len(finished_queue) == len(processes):
            print("all processes have finished")
            average_waiting_time = 0
            for process in finished_queue:
                print(f"process {process.id} waiting time is {process.waiting_time}")
                average_waiting_time += process.waiting_time
            average_waiting_time /= len(processes)
            print(f"average waiting time is {average_waiting_time}")
            os._exit(0)
            


if __name__ == "__main__":
    read_processes()
    open('RR1.txt', 'w').close()
    with open("RR1.txt", "a") as file:
        print("initial processes", file=file)
        for process in processes:
            print(process, file=file)
        print("------------------------------------------------", file=file)
    open('RR2.txt', 'w').close()
    with open("RR2.txt", "a") as file:
        print("initial processes", file=file)
        for process in ready_queue_2.queue:
            print(process, file=file)
        print("------------------------------------------------", file=file)
    open('SRTF.txt', 'w').close()
    open('waiting_queue_1.txt', 'w').close()
    open('finished_queue.txt', 'w').close()
    thread1 = Thread(target=enqueue)
    thread2 = Thread(target=CPU)
    thread3 = Thread(target=check_all_waiting_queues)
    thread4 = Thread(target=debug)
    thread5 = Thread(target=end)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
