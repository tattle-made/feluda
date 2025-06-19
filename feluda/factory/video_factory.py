import os
import tempfile

import wget
from werkzeug.datastructures import FileStorage

from feluda.factory.s3_factory import S3Factory


class VideoFactory:
    @staticmethod
    def make_from_url(video_url: str) -> dict:
        temp_dir = tempfile.gettempdir()

        if video_url.startswith("http"):
            temp_url = video_url.split("?", maxsplit=1)[0]
            file_name = temp_url.split("/")[-1] + ".mp4"
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading video from URL")
                wget.download(video_url, out=file_path)
                print("\nVideo downloaded")
            except Exception as e:
                print("Error downloading video:", e)
                raise Exception("Error Downloading Video")
        else:
            bucket_name = S3Factory.aws_bucket
            file_key = video_url
            file_name = file_key.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading video from S3")
                S3Factory.download_file_from_s3(bucket_name, file_key, file_path)
                print("\nVideo downloaded")
            except Exception as e:
                print("Error downloading video from S3:", e)
                raise Exception("Error Downloading Video")

        return {"path": file_path}

    @staticmethod
    def make_from_file_on_disk(video_path: str) -> dict:
        return {"path": video_path}

    @staticmethod
    def make_from_file_in_memory(file_data: FileStorage) -> dict:
        # save on disk
        fname = tempfile.gettempdir() + os.sep + file_data.filename
        file_data.save(fname)
        return {"path": fname}
