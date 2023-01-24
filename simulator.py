from queue import Queue
from threading import Thread
import time
from workload import Process

class Process:
    def __init__(self, id: int, arrival_time: int, bursts: list[int]) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.brusts = bursts
        self.rank = 1
        self.waiting = False
    def __str__(self) -> str:
        return f"{self.id} {self.arrival_time} {' '.join([str(brust) for brust in self.brusts])}"

    def run(self, time_quantum: int = 0):
        burst = self.brusts[0]
        timer = 0
        while timer < time_quantum:
            print(f"Process {self.id} is running")
            timer += 1
            burst -= 1
            time.sleep(1)
        if burst > 0:
            self.brusts[0] = burst
        else:
            self.brusts.pop(0)
            if len(self.brusts) > 0:
                self.waiting = True
                Waiting.put(self)
            
def read_processes(filename: str) -> list[Process]:
    processes = []
    with open(filename) as f:
        for line in f:
            processes.append(Process(*[int(x) for x in line.split()]))
    return processes

Queue1 = Queue()
Queue2 = Queue()
Queue3 = Queue()
Queue4 = Queue()
Waiting = Queue()
ready_queue = Queue()
processes = read_processes("processes.txt")
def scheduler():
    while True:
        if not Queue1.empty():
            process = Queue1.get()
            process.run()
            Queue1.task_done()
        elif not Queue2.empty():
            process = Queue2.get()
            process.run()
            Queue2.task_done()
        elif not Queue3.empty():
            process = Queue3.get()
            process.run()
            Queue3.task_done()
        elif not Queue4.empty():
            process = Queue4.get()
            process.run()
            Queue4.task_done()
        elif not Waiting.empty():
            process = Waiting.get()
            process.run()
            Waiting.task_done()
        else:
            time.sleep(1)
        
def add_processes(): # This is a thread that addes processes to thier respective queues
    while True:
        for process in :
            if process.arrival_time == time:
                if process.rank == 1:
                    Queue1.put(process)
                elif process.rank == 2:
                    Queue2.put(process)
                elif process.rank == 3:
                    Queue3.put(process)
                elif process.rank == 4:
                    Queue4.put(process)
def round_robin(Queue: Queue, time_quantum: int): # This is a thread that runs the round robin algorithm
    while True:
        if not Queue.empty():
            process = Queue.get()
            process.run()
            Queue.task_done()

        else:
            sleep(1)