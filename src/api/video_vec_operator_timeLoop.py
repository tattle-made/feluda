import time
from core.operators import vid_vec_rep_resnet

def find_time(num_iterations):
    file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
    vid_vec_rep_resnet.initialize(param=None)
    durations = []
    for _ in range(num_iterations):
        start_time = time.time()
        vid_vec_rep_resnet.run(file_path)
        end_time = time.time()
        duration = end_time - start_time
        durations.append(duration)
    durations.sort()
    total_duration = sum(durations)
    average_duration = total_duration / num_iterations
    if num_iterations % 2 == 0:
        median_duration = (durations[num_iterations // 2 - 1] + durations[num_iterations // 2]) / 2
    else:
        median_duration = durations[num_iterations // 2]
    highest_duration = max(durations)
    print(f"Average time taken for {num_iterations} iterations: {average_duration:.6f} seconds")
    print(f"Median time taken for {num_iterations} iterations: {median_duration:.6f} seconds")
    print(f"Highest time taken for {num_iterations} iterations: {highest_duration:.6f} seconds")
    print("Video vec time profile complete!")

if __name__ == "__main__":
    find_time(5)