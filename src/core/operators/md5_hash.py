
def initialize(param):
    global hashlib
    import hashlib

def run(media_path):
    file_path = media_path["path"]
    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        # file_hash = hashlib.blake2b()
        while chunk := f.read(4092):
            file_hash.update(chunk)
    
    return file_hash.hexdigest()

# if __name__ == "__main__":
#     media_file_path = r'sample_data/sample-cat-video.mp4'
#     initialize(param={})
#     md5_hash = run(media_file_path)
#     print(md5_hash)
#     print(len(md5_hash))