import random


class Process:
    def __init__(self, id: int, arrival_time: int, bursts: list[int], waiting_time: int = 0, counter: int = 0,queue:int=1,predicted_time:float=0):
        self.id = id
        self.arrival_time = arrival_time
        self.bursts = bursts
        self.waiting_time = waiting_time
        self.counter = counter
        self.queue=queue
        self.predicted_time=predicted_time

    def __str__(self):
        return f"{self.id} {self.arrival_time} {' '.join([str(burst) for burst in self.bursts])}"


processes_count: int = int(input("Enter the number of processes: "))
max_time: int = int(input("Enter the maximum arrival time: "))
max_cpu_bursts: int = int(input("Enter the maximum number of CPU bursts: "))
min_io_time: int = int(input("Enter the minimum IO time: "))
max_io_time: int = int(input("Enter the maximum IO time: "))
min_cpu_time: int = int(input("Enter the minimum CPU time: "))
max_cpu_time: int = int(input("Enter the maximum CPU time: "))
processes: list[Process] = []

for i in range(1, processes_count + 1):
    arrival_time = random.randint(0, max_time)
    cpu_bursts = random.randint(1, max_cpu_bursts)
    bursts = []
    # print(f"Process {i} has {cpu_bursts} CPU bursts")
    for j in range(cpu_bursts):
        bursts.append(random.randint(min_cpu_time, max_cpu_time))
        if j != cpu_bursts - 1:
            bursts.append(random.randint(min_io_time, max_io_time))
    processes.append(Process(i, arrival_time, bursts))

with open("processes.txt", "w") as file:
    for process in processes:
        print(process, file=file)






        
