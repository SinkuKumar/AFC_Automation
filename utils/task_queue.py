import os
import sys
import time
import queue
import threading
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.pyodbc_sql import PyODBCSQL

class TaskQueue:
    def __init__(self):
        """Initializes a task queue."""
        self.task_queue = queue.Queue()
        self.worker_thread = None
        self.lock = threading.Lock()  # Prevents race conditions
        self.error = None

    def _process_queue(self):
        """
        Worker thread to retrieve the tasks from the queue
        and execute the functions with the provided arguments.
        """
        while True:
            try:
                func, args, kwargs = self.task_queue.get(timeout=1)

                if self.error:
                    self.task_queue.task_done()
                    continue 

                try:
                    func(*args, **kwargs)
                except Exception as e:
                    self.error = e
                    print(f"Error executing task: {e}")  # Log the error but continue

                self.task_queue.task_done()
            except queue.Empty:
                with self.lock:
                    if self.task_queue.unfinished_tasks == 0:
                        self.worker_thread = None  # Allow restart later
                        break  # Exit thread if no tasks remain


    def _ensure_worker_running(self):
        """Ensure worker thread is running."""
        with self.lock:
            if self.worker_thread is None or not self.worker_thread.is_alive():
                self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
                # self.worker_thread = threading.Thread(target=self._process_queue)
                self.worker_thread.start()

    def add_task(self, func, *args, **kwargs):
        """Add a task and start the worker if necessary."""
        if self.error:
            return
        
        self.task_queue.put((func, args, kwargs))
        self._ensure_worker_running()

    def check_and_raise_error(self):
        """Check if any task failed, and raise the error in the main thread."""
        error_message = None
        if self.error:
            error_message = self.error
            self.error = None
        return error_message

    def wait_for_completion(self):
        """Wait until all tasks in the queue are processed before exiting."""
        self.task_queue.join()


# Example Usage
if __name__ == "__main__":
    def example_task(name):
        print(f"Task {name} started")
        time.sleep(5)
        print(f"Task {name} completed")

    queue_manager = TaskQueue()

    queue_manager.add_task(example_task, "A")
    queue_manager.add_task(example_task, "B")

    # time.sleep(40)  # Simulate some wait time

    queue_manager.add_task(example_task, "C")  # This will automatically restart the worker
    print("\nWaiting for completion")
    queue_manager.wait_for_completion()
    print("Queue ended")
