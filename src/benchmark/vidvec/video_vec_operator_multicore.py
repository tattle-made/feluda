from multiprocessing import Process
from multiprocessing import cpu_count
from core.operators import vid_vec_rep_resnet
import time


def find_time():
    file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
    start_time = time.time()
    vid_vec_rep_resnet.run(file_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken - {duration}")
    print("Video vec time profile complete!")


N = 4
total_cores = cpu_count()

print("number of cpus: ", cpu_count())
print("distribute test on", int(total_cores / N), "cores")

processes = []

vid_vec_rep_resnet.initialize(param=None)

for core in range(int(total_cores / N)):
    proc = Process(target=find_time)
    processes.append(proc)
    proc.start()

for proc in processes:
    proc.join()
