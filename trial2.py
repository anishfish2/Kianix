import time
import multiprocessing

def write_data(data_queue):
    try:
        while True:
            data = "Data to be written"
            data_queue.put(data)
            print("Data added to queue:", data)
            time.sleep(1)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Writer script interrupted")

if __name__ == "__main__":
    data_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=write_data, args=(data_queue,))
    process.start()
    process.join()