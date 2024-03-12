def initialize(param):
    global hashlib
    import hashlib


def run(media_path):
    file_path = media_path["path"]
    with open(file_path, "rb") as f:
        file_hash = hashlib.blake2b()
        while chunk := f.read(4092):
            file_hash.update(chunk)

    return file_hash.hexdigest()


# if __name__ == "__main__":
#     media_file_path = {"path": r"core/operators/sample_data/sample-cat-video.mp4"}
#     initialize(param={})
#     file_hash = run(media_file_path)
#     print(file_hash)
#     print(len(file_hash))
