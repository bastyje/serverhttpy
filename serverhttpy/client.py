import requests
import multiprocessing as mp


processes = list()
for i in range(10):
    processes.append(
        mp.Process(target=lambda: requests.post("http://127.0.0.1:8080/movie"))
    )
    processes[i].start()

for i in range(10):
    processes[i].join()
