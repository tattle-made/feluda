import core.operators.vid_vec_rep_resnet


def profile_code():
    file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
    core.operators.vid_vec_rep_resnet.initialize(param=None)
    core.operators.vid_vec_rep_resnet.run(file_path)
    print("Video vec profiler complete!")


if __name__ == "__main__":
    profile_code()
