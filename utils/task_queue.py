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
        self.task_queue = queue.Queue()
        self.worker_thread = None
        self.lock = threading.Lock()  # Prevents race conditions

    def _process_queue(self):
        while True:
            try:
                func, args, kwargs = self.task_queue.get(timeout=1)
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Error executing task: {e}")  # Log the error but continue
    
                self.task_queue.task_done()
            except queue.Empty:
                with self.lock:
                    if self.task_queue.unfinished_tasks == 0:
                        self.worker_thread = None  # Allow restart later
                        break  # Exit thread if no tasks remain


    def _ensure_worker_running(self):
        with self.lock:
            if self.worker_thread is None or not self.worker_thread.is_alive():
                self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
                self.worker_thread.start()

    def add_task(self, func, *args, **kwargs):
        """Add a task and start the worker if necessary."""
        self.task_queue.put((func, args, kwargs))
        self._ensure_worker_running()


# Example Usage
if __name__ == "__main__":
    def example_task(name):
        print(f"Task {name} started")
        time.sleep(2)
        print(f"Task {name} completed")

    queue_manager = TaskQueue()
    
    queue_manager.add_task(example_task, "A")
    queue_manager.add_task(example_task, "B")

    time.sleep(40)  # Simulate some wait time
    
    queue_manager.add_task(example_task, "C")  # This will automatically restart the worker
