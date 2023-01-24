import random
from time import sleep
from simulator import Process
processes_count: int = int(input("Enter the number of processes: "))
max_time: int = int(input("Enter the maximum arrival time: "))
max_cpu_brusts: int = int(input("Enter the maximum number of CPU brusts: "))
min_io_time: int = int(input("Enter the minimum IO time: "))
max_io_time: int = int(input("Enter the maximum IO time: "))
min_cpu_time: int = int(input("Enter the minimum CPU time: "))
max_cpu_time: int = int(input("Enter the maximum CPU time: "))
proccesses: list[Process] = []

for i in range(1, processes_count + 1):
    arrival_time = random.randint(0, max_time)
    cpu_bursts = random.randint(1, max_cpu_brusts)
    bursts = []
    for j in range(cpu_bursts):
        bursts.append(random.randint(min_cpu_time, max_cpu_time))
        if j != cpu_bursts - 1:
            bursts.append(random.randint(min_io_time, max_io_time))
    proccesses.append(Process(i, arrival_time, bursts))

with open("processes.txt", "w") as file:
    for process in proccesses:
        print(process, file=file)
