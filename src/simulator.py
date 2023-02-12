import os
from queue import Queue
from threading import Thread, Event
from time import sleep
from workload import Process, read_processes
from matplotlib import pyplot as plt
Queue1 = Queue()
Queue2 = Queue()
Queue3 = []
Queue4 = Queue()
Queues = [Queue1, Queue2, Queue3, Queue4]
Waiting: list[Process]= []
Finished: list[Process]= []

def gantt_chart(data):
    #data[i] = (process_id,color id ,start_time, end_time)
    colors={0:'white',1:'red',2:'blue',3:'green',4:'yellow'}
    fig, ax = plt.subplots()
    for i in data:
        process_id=i[0]
        queue_color=colors[i[1]]
        start_time=i[2]
        end_time=i[3]
        rec = plt.Rectangle((start_time, 0), end_time - start_time, 1, facecolor=queue_color, edgecolor='black', label=f"P{process_id}")
        #add process id to the rectangle in the gantt chart in the middle of the rectangle
        if i[1] != 0:
            ax.text((start_time + end_time) / 2, 0.5, f"P{process_id}", ha='center', va='center', color='black')
        ax.add_patch(rec)
        #add text to the rectangle with the start time and end time of the process
    ax.set_xlim(0, data[-1][3])
    ax.set_ylim(0, 1)
    ax.set_xlabel('Time')
    
    plt.show()

    
    

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

def clock():
    global global_timer, running_process, num_processes
    dict = []
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
        dict.append([running_process.id,running_process.rank,global_timer] if running_process != None else [0,0,global_timer])
        for t in threads:
            t.event.set()
        for t in threads:
            t.event.clear()
        sleep(0.01)
        print("Time:  ", global_timer)
        print("Queue 1: ", [x.id for x in list(Queue1.queue)])
        print("Queue 2: ", [x.id for x in list(Queue2.queue)])
        print("Queue 3: ", [x.id for x in Queue3])
        print("Waiting: ", [x.id for x in Waiting])
        print("Running: ", running_process.id if running_process else None)
        print("Finished: ", [x.id for x in Finished])
        if len(Finished) == num_processes:
            data=[]
            current=[dict[0][0],dict[0][1],dict[0][2],dict[0][2]]
            for i in dict[1:]:
                if i[0]==current[0] and i[1]==current[1]:
                    current[3]=i[2]+1
                else:
                    data.append((current[0],current[1],current[2],current[3]))
                    current=[i[0],i[1],i[2],i[2]]
            data.append((current[0],current[1],current[2],current[3]))
            global_timer = -1
            for i in data:
                print(i)
            gantt_chart(data)
            print(sum([x.waiting_time for x in Finished]) / len(Finished))
            os._exit(0)
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
    global_timer = 0
    running_process = None
    threads = []
    targets = [waiting, running,]
    q1 = int(input("Enter time quantam for RR1: "))
    q2 = int(input("Enter time quantam for RR2: "))
    alpha = float(input("Enter alpha [0 - 1]: ")) 
    for target in targets:
        event = Event()
        t = Thread(target=target)
        t.event = event
        threads.append(t)
        t.start()
    Thread(target=clock).start()
