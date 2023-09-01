import time
import multiprocessing

def read_data(data_queue):
    try:
        while True:
            if not data_queue.empty():
                data = data_queue.get()
                print("Read data:", data)
            time.sleep(5)  # Adjust the interval as needed
    except KeyboardInterrupt:
        print("Reader script interrupted")

if __name__ == "__main__":
    data_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=read_data, args=(data_queue,))
    process.start()
    process.join()
