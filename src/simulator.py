import os
from queue import Queue
from threading import Thread, Event
from time import sleep
from gui_test import CPU_Scheduling_GUI
from workload import Process, read_processes
from gui_test import  run_gui
from PyQt5.QtCore import QTimer
import sys
from PyQt5.QtWidgets import *

def get_next_queue(process: Process):
    global alpha, q1, q2
    if process.rank == 1 and process.running_time >= 10  * q1:
        process.rank = 2
        process.running_time = 0
    elif process.rank == 2 and process.running_time >= 10 * q2:
        process.rank = 3
        process.predicted_time = alpha * process.bursts[0] + (1 - alpha) * process.predicted_time
        process.running_time = 0
    elif process.rank == 3:
        process.predicted_time = alpha * process.bursts[0] + (1 - alpha) * process.predicted_time
    Queues[process.rank - 1].put(process) if process.rank != 3 else Queue3.append(process)
    print("📥\t\tProcess ", process.id, " is enqueued at time ", global_timer, "ms")
def clock()
    global global_timer, running_process, num_processes, gui    
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
                        get_next_queue(process)
                        if process in Waiting:
                            Waiting.remove(process)
                    to_remove.append(process)
            
            if to_append is not None:
                get_next_queue(to_append)
                to_append = None
                
            if running_process is not None:
                if not Queue1.empty(): # For preemption
                    if running_process.rank > 1:
                        Queues[running_process.rank - 1].put(running_process) if running_process.rank != 3 else Queue3.append(running_process)
                        running_process.status = "Ready"
                        running_process = Queue1.get()
                        running_process.status = "Running"
                        running_process.quantum = q1
                        print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")

                elif  not Queue2.empty():
                    if running_process.rank > 2: # For preemption
                        Queues[running_process.rank - 1].put(running_process) if running_process.rank != 3 else Queue3.append(running_process)
                        running_process.status = "Ready"
                        running_process = Queue2.get()
                        running_process.status = "Running"
                        running_process.quantum = q2
                        print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
                elif len(Queue3):
                    Queue3.sort(key=lambda x: x.predicted_time)
                    if running_process.rank >= 3: # For preemption
                        if running_process.predicted_time > Queue3[0].predicted_time:
                            running_process.counter += 1
                            if running_process.counter == 3:
                                running.process.rank = 4
                            Queues[running_process.rank - 1].put(running_process) if running_process.rank != 3 else Queue3.append(running_process)
                            running_process.status = "Ready"
                            running_process = Queue3.pop(0)
                            running_process.status = "Running"
                            running_process.quantum = running_process.bursts[0]
                            print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.bursts[0], "ms")
            else:
                if not Queue1.empty(): # Running process is None so we can run a new process
                    running_process = Queue1.get()
                    running_process.status = "Running"
                    running_process.quantum = q1
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
                elif not Queue2.empty(): # Running process is None so we can run a new process
                    running_process = Queue2.get()
                    running_process.status = "Running"
                    running_process.quantum = q2
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.quantum, "ms")
                elif len(Queue3):
                    Queue3.sort(key=lambda x: x.predicted_time)
                    running_process = Queue3.pop(0)
                    running_process.status = "Running"
                    running_process.quantum = running_process.bursts[0]
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.bursts[0], "ms")
                elif not Queue4.empty():
                    running_process = Queue4.get()
                    running_process.status = "Running"
                    running_process.quantum = running_process.bursts[0]
                    print("🏃\t\tProcess ", (running_process.id, running_process.rank), " is running at time ", global_timer, "ms for ", running_process.bursts[0], "ms")
            for i, q in enumerate(Queues):
                if i == 2:
                    for elem in Queue3:
                        elem.waiting_time += 1
                else:
                    for elem in list(q.queue):
                        elem.waiting_time += 1
            for process in to_remove:
                processes.remove(process)
            for t in threads:
                t.event.set()
            for t in threads:
                t.event.clear()
            sleep(0.05)
            if gui:
                Queue1_str = " ".join([f"P{i.id}" for i in list(Queue1.queue)])
                Queue2_str = " ".join([f"P{i.id}" for i in list(Queue2.queue)])
                Queue3_str = " ".join([f"P{i.id}" for i in Queue3])
                Queue4_str = " ".join([f"P{i.id}" for i in list(Queue4.queue)])
                Waiting_str = " ".join([f"P{i.id}" for i in Waiting])
                Finished_str = " ".join([f"P{i.id}" for i in Finished])
                gui.update_queues(Queue1_str, Queue2_str, Queue3_str, Queue4_str,Waiting_str, running_process, Finished_str, global_timer)
            print("Time:  ", global_timer)
            print("Queue 1: ", [x.id for x in list(Queue1.queue)])
            print("Queue 2: ", [x.id for x in list(Queue2.queue)])
            print("Queue 3: ", [x.id for x in Queue3])
            print("Waiting: ", [x.id for x in Waiting])
            print("Running: ", running_process.id if running_process else None)
            print("Finished: ", [x.id for x in Finished])
            if len(Finished) == num_processes:
                global_timer = -1
                print("Average waiting time: ", sum([x.waiting_time for x in Finished]) / len(Finished))
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
            running_process.bursts[0] -= 1
            running_process.quantum -= 1
            running_process.running_time += 1
            if running_process.quantum == 0 or running_process.bursts[0] == 0:
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
    gui = None
    global_timer = 0
    running_process = None
    threads = []
    targets = [waiting, running]
    q1 = int(input("Enter time quantam for RR1: "))
    q2 = int(input("Enter time quantam for RR2: "))
    alpha = float(input("Enter alpha [0 - 1]: ")) 
    Queue1 = Queue()
    Queue2 = Queue()
    Queue3 = []
    Queue4 = Queue()
    Queues = [Queue1, Queue2, Queue3, Queue4]
    Waiting: list[Process]= []
    Finished: list[Process]= []
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    app = QApplication(sys.argv)
    gui = CPU_Scheduling_GUI()
    Thread(target=clock).start()    
    gui.show()
    sys.exit(app.exec_())
