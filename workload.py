import random


class Process:
    def __init__(self, id: int, arrival_time: int, brusts: list[int]):
        self.id = id
        self.arrival_time = arrival_time
        self.brusts = brusts

    def __str__(self):
        return f"{self.id} {self.arrival_time} {' '.join([str(brust) for brust in self.brusts])}"


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
    cpu_brusts = random.randint(1, max_cpu_brusts)
    brusts = []
    # print(f"Process {i} has {cpu_brusts} CPU brusts")
    for j in range(cpu_brusts):
        brusts.append(random.randint(min_cpu_time, max_cpu_time))
        if j != cpu_brusts - 1:
            brusts.append(random.randint(min_io_time, max_io_time))
    proccesses.append(Process(i, arrival_time, brusts))

with open("processes.txt", "w") as file:
    for process in proccesses:
        print(process, file=file)
