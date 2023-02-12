import threading
import time

# Define the clock thread
def clock():
    while True:
        print("Clock: Ticking...")
        time.sleep(1)
        # Send signal to other threads
        for t in threads:
            t.event.set()
        # Reset event for next iteration
        for t in threads:
            t.event.clear()

# Define the sequential threads
def sequential(id):
    i = 0
    while True:
        # Wait for signal from clock
        event.wait()
        print(f"Thread {id}: is running {i}")
        i += 1 

# Create a list to store the threads
threads = []

# Create and start the sequential threads
for i in range(3):
    event = threading.Event()
    t = threading.Thread(target=sequential, args=(i,))
    t.event = event
    threads.append(t)
    t.start()

# Create and start the clock thread
ct = threading.Thread(target=clock)
ct.start()
