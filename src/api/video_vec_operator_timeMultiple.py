import requests
import os
import time
import random
from dotenv import load_dotenv
from core.operators import vid_vec_rep_resnet
load_dotenv(dotenv_path="drivelink.env")

def download_file(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def find_time(file_path):
    vid_vec_rep_resnet.initialize(param=None)
    start_time = time.time()
    vid_vec_rep_resnet.run(file_path)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Time taken by {file_path['path']} - {duration} seconds")

if __name__ == "__main__":
    drive_links = [os.getenv(f"DRIVE_LINK_{i}") for i in range(1, 6)]
    filenames = ['video-10sec.mp4', 'video-30sec.mp4', 'video-60sec.mp4', 'video-300sec.mp4', 'video-600sec.mp4']
    indices = list(range(len(drive_links)))
    random.shuffle(indices)
    for index in indices:
        drive_link = drive_links[index]
        filename = filenames[index]
        download_file(drive_link, filename)
        file_path = {"path": filename}
        print(f"Processing {filename}...")
        find_time(file_path)