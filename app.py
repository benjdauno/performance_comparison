import time
import math
import threading
import random
import string
import gevent
import os

from flask import Flask

app = Flask(__name__)
file_name = "/tmp/test_file.txt"
with open(file_name, 'w') as f:
    for _ in range(10000):
        f.write(random.choice(string.ascii_letters) + "\n")
# Endpoint 1: CPU and memory consumption with finite loop duration
@app.route('/cpu_memory1')
def cpu_memory1():
    """Simulate CPU load with a busy loop and memory consumption for a limited time."""
    
    def busy_loop(duration=5):
        """Run a busy loop for a specified duration to simulate CPU consumption."""
        end_time = time.time() + duration
        while time.time() < end_time:
            pass  # Busy loop to consume CPU
    
    async def memory_intensive():
        """Create large data structures to consume memory."""
        data = []
        for _ in range(1000):
            # Generate random strings and append to list
            data.append(''.join(random.choices(string.ascii_uppercase + string.digits, k=1000)))
        await asyncio.sleep(2)  # Let the memory usage settle

    # Run both CPU and memory-intensive tasks in separate threads
    cpu_thread = threading.Thread(target=busy_loop)
    memory_thread = threading.Thread(target=memory_intensive)

    cpu_thread.daemon = True
    memory_thread.daemon = True

    cpu_thread.start()
    memory_thread.start()
    cpu_thread.join()
    memory_thread.join()
    return "CPU and memory are being consumed by busy loop (for 5 seconds) and large data structures."

# Endpoint 2: Heavy math computation and file I/O
@app.route('/cpu_memory_io2')
def cpu_memory_io2():
    """Simulate CPU load with math, memory, and file I/O."""
    # CPU load with heavy math operations
    result = 0
    for i in range(1, 1000000):
        result += math.sqrt(i)

    # Memory-intensive task: Create large list
    data = [''.join(random.choices(string.ascii_uppercase + string.digits, k=1000)) for _ in range(1000)]

    # File I/O: Write large data to a file
    file_name = "/tmp/test_file.txt"
    with open(file_name, 'w') as f:
        for _ in range(1000000):
            f.write(random.choice(string.ascii_letters) + "\n")
    
    return f"Computed math, created large data structures, and wrote to file: {file_name}"

# Endpoint 3: Sleeping with I/O-bound task (file operations and sleeping)
@app.route('/cpu_memory_io3')
def cpu_memory_io3():
    """Simulate I/O by sleeping and doing file operations."""
    # File I/O: Read large file
    file_name = "/tmp/test_file.txt"
    
    with open(file_name, 'r') as f:
        lines = f.readlines()

    # Sleep to simulate I/O delay
    gevent.sleep(.15)

    return f"Read file {file_name} and slept for I/O simulation."

# Don't call app.run() here; Gunicorn will manage it.
