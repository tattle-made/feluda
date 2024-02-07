import time
from core.operators import vid_vec_rep_resnet

def find_time():
    file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
    vid_vec_rep_resnet.initialize(param=None)
    start_time = time.time()
    vid_vec_rep_resnet.run(file_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken - {duration}")

if __name__ == "__main__":
    find_time()