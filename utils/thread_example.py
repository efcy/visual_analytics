import queue
import threading
import os

def write_to_queue(data_queue, data):
    data_queue.put(data)

def worker(data_queue, output_directory):
    while True:
        try:
            data = data_queue.get(timeout=5)  # Wait for 5 seconds for new data
            filename = f"{threading.current_thread().name}_{data_queue.qsize()}.txt"
            filepath = os.path.join(output_directory, filename)
            
            with open(filepath, 'w') as file:
                file.write(data)
            
            data_queue.task_done()
        except queue.Empty:
            break  # Exit if no new data for 5 seconds

def main():
    data_queue = queue.Queue()
    output_directory = "output_files"
    num_threads = 5

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Create and start worker threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(data_queue, output_directory))
        t.start()
        threads.append(t)

    # Example: Write some data to the queue
    for i in range(20):
        write_to_queue(data_queue, f"Data item {i}")

    # Wait for all tasks to be completed
    data_queue.join()

    # Stop worker threads
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()