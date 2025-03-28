import time
import queue
import threading

class TaskQueue:
    def __init__(self, max_retries=3):
        """Initializes a task queue with retry capability."""
        self.task_queue = queue.Queue()
        self.worker_thread = None
        self.lock = threading.Lock()  # Prevents race conditions
        self.max_retries = max_retries  # Maximum number of retries per task
        self.retry_count = {}  # Keeps track of retries per task

    def _process_queue(self):
        """Worker thread to retrieve and execute tasks."""
        while True:
            try:
                func, args, kwargs, on_failure = self.task_queue.get(timeout=1)
                try:
                    func(*args, **kwargs)  # Execute the function
                except Exception as e:
                    print(f"Error executing task {args}: {e}")  # Log the error
                    if on_failure:
                        on_failure(e, func, *args, **kwargs)  # Call failure callback

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
                self.worker_thread.start()

    def add_task(self, func, *args, on_failure=None, **kwargs):
        """Add a task with an optional failure callback."""
        self.retry_count[args] = self.retry_count.get(args, 0)  # Initialize retry count
        self.task_queue.put((func, args, kwargs, on_failure))
        self._ensure_worker_running()

    def wait_for_completion(self):
        """Wait until all tasks in the queue are processed before exiting."""
        self.task_queue.join()

    def retry_task(self, error, func, *args, **kwargs):
        """Handles task retry logic by adding it back to the queue if retries are left."""
        if self.retry_count[args] < self.max_retries:
            self.retry_count[args] += 1
            print(f"Retrying task {args} ({self.retry_count[args]}/{self.max_retries})...")
            self.add_task(func, *args, on_failure=self.retry_task, **kwargs)
        else:
            print(f"Task {args} failed after {self.max_retries} retries.")


# Example Usage
if __name__ == "__main__":
    def example_task(name):
        print(f"Task {name} started")
        time.sleep(2)
        if name == "B":
            raise ValueError("Simulated Failure")  # Simulate an error
        print(f"Task {name} completed")

    queue_manager = TaskQueue(max_retries=3)

    queue_manager.add_task(example_task, "A", on_failure=queue_manager.retry_task)
    queue_manager.add_task(example_task, "B", on_failure=queue_manager.retry_task)
    queue_manager.add_task(example_task, "C", on_failure=queue_manager.retry_task)
    queue_manager.wait_for_completion()
    print("Queue ended")
