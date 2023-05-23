import requests
import multiprocessing as mp
import time

processes = list()
start = time.time()
for i in range(10):
    processes.append(
        mp.Process(target=lambda: requests.post("http://127.0.0.1:8080/"))
    )
    processes[i].start()

for i in range(10):
    processes[i].join()

end = time.time()
print(f"elapsed time: {end - start}s\n")