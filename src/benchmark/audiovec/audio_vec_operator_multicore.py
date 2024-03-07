from multiprocessing import Process
from multiprocessing import cpu_count
import time
from core.operators import audio_vec_embedding


def find_time():
    file_path = {"path": r"core/operators/sample_data/audio.wav"}
    audio_vec_embedding.initialize(param=None)
    start_time = time.time()
    audio_vec_embedding.run(file_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken - {duration}")


N = 1
total_cores = cpu_count()

print("number of cpus: ", cpu_count())
print("distribute test on", int(total_cores / N), "cores")

processes = []

audio_vec_embedding.initialize(param=None)

for core in range(int(total_cores / N)):
    proc = Process(target=find_time)
    processes.append(proc)
    proc.start()

for proc in processes:
    proc.join()
