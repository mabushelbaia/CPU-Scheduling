import random


class Process:
    def __init__(self, id: int, arrival_time: int, bursts: list[int]) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.brusts = bursts
        self.rank = 1
        self.waiting = False
        self.counter = 0
        self.waiting_time = 0

    def __str__(self) -> str:
        return f"{self.id} {self.arrival_time} {' '.join([str(brust) for brust in self.brusts])}"


def read_processes(filename: str) -> list[Process]:
    processes = []
    with open(filename) as f:
        for line in f:
            process = line.split()
            processes.append(Process(int(process[0]), int(process[1]), [
                             int(brust) for brust in process[2:]]))
    return processes


def write_processes(filename: str) -> None:
    processes_count: int = int(input("Enter the number of processes: "))
    max_time: int = int(input("Enter the maximum arrival time: "))
    max_cpu_bursts: int = int(
        input("Enter the maximum number of CPU bursts: "))
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
    with open(filename, "w") as file:
        for process in sorted(processes, key=lambda process: process.arrival_time):
            print(process, file=file)


if __name__ == "__main__":
    write_processes("processes.txt")
