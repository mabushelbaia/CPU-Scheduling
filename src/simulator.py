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
running_process:Process = None
stop_threads = False
no_interrupts = True
flags = [True, True, True, True]
time_quantum_1=int(input("Enter the time quantum for queue 1: "))
time_quantum_2=int(input("Enter the time quantum for queue 2: "))


def clock():
    global global_timer
    while True:
        print("Clock: Ticking...")
        sleep(1)
        # Send signal to other threads
        for t in threads:
            t.event.set()
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
        event.clear()


def running():
    while True:
        if not Queue1.empty:
            running_process = Queue1.get()
            counter = 0
            while counter < time_quantum_1 and running_process.bursts[0]>0 and len(running_process.bursts)>0:
                running_process.bursts[0]-=1
                running_process.counter+=1
                counter+=1
                if running_process.bursts[0]==0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts)>0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if running_process.counter==10*time_quantum_1:
                    running_process.rank+=1
                    running_process.counter=0
                    Queue2.put(running_process)
                    break
                if running_process.bursts[0]>0 and counter==time_quantum_1:
                    Queue1.put(running_process)
                    break
        elif Queue1.empty() and not Queue2.empty():
            running_process = Queue2.get()
            counter = 0
            while counter < time_quantum_2 and running_process.bursts[0]>0 and len(running_process.bursts)>0:
                running_process.bursts[0]-=1
                running_process.counter+=1
                counter+=1
                if not Queue1.empty():
                    Queue2.put(running_process)
                    break
                if running_process.bursts[0]==0:
                    running_process.bursts.pop(0)
                    if len(running_process.bursts)>0:
                        Waiting.append(running_process)
                        break
                    else:
                        Finished.append(running_process)
                        break
                if running_process.counter==10*time_quantum_2:
                    running_process.rank+=1
                    Queue3.put(running_process)
                    break
                if running_process.bursts[0]>0 and counter==time_quantum_2:
                    Queue2.put(running_process)
                    break
                    
    
                    
                
                
                
                        
                        
            
        


if __name__ == "__main__":
    processes = read_processes("processes.txt")
    threads = []
    event = Event()
    t = Thread(target=enqueue)
    t.event = event
    threads.append(t)
    t.start()
    control_thread = Thread(target=clock)
    control_thread.start()
