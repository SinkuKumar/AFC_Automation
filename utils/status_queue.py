import multiprocessing
import time
import random

# File to store records
FILE_PATH = "records.txt"

def worker(queue):
    """ Function to process queue and write data sequentially to a file """
    with open(FILE_PATH, "a") as f:  # Open file in append mode
        while True:
            data = queue.get()  # Get data from queue
            if data is None:  # Stop condition
                break
            f.write(f"{data}\n")
            f.flush()  # Ensure immediate write
            print(f"Written to file: {data}")

def process_task(queue, process_id):
    """ Simulated worker process adding data to queue """
    for i in range(5):  # Each process adds multiple records
        record = f"Process-{process_id}: Record-{i}"
        queue.put(record)
        print(f"Process-{process_id} added: {record}")
        time.sleep(random.uniform(0.5, 1.5))  # Simulating work delay

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    # Start worker process
    worker_process = multiprocessing.Process(target=worker, args=(queue,))
    worker_process.start()

    # Create multiple processes to generate records
    processes = []
    num_processes = 5  # Number of processes simulating different calls
    for i in range(num_processes):
        p = multiprocessing.Process(target=process_task, args=(queue, i))
        p.start()
        processes.append(p)

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Send stop signal to worker
    queue.put(None)
    worker_process.join()

    print("All processes completed. Check records.txt for results.")
