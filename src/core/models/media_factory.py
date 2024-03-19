import requests
from requests.exceptions import ConnectTimeout
import PIL
from io import BytesIO
import numpy as np
from werkzeug.datastructures import FileStorage
import wget
from core.models.media import MediaType
import logging
import os
import tempfile
import boto3

log = logging.getLogger(__name__)


class ImageFactory:
    @staticmethod
    def make_from_url(image_url):
        try:
            print("1", image_url)
            resp = requests.get(image_url, timeout=(3.05, 5))
            image_bytes = resp.content
            image = PIL.Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {"image": image, "image_array": image_array, "image_bytes": image_bytes}
        except ConnectTimeout:
            print('Request has timed out')

    @staticmethod
    def make_from_file_on_disk(image_path):
        with open(image_path, mode="rb") as file:
            image_bytes = file.read()
            image = PIL.Image.open(BytesIO(image_bytes))
            image_array = np.array(image)
            return {
                "image": image,
                "image_array": image_array,
                "image_bytes": image_bytes,
            }

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage):
        image_bytes = image_data.read()
        image = PIL.Image.open(BytesIO(image_bytes))
        image_array = np.array(image)
        return {
            "image": image,
            "image_array": image_array,
            "image_bytes": image_bytes,
        }


class TextFactory:
    @staticmethod
    def make_from_url(text_url):
        try:
            response = requests.get(text_url, timeout=(3.05, 5))
            text = response.text
            return {"text": text}
        except ConnectTimeout:
            print('Request has timed out')

    @staticmethod
    def make_from_file_on_disk(image_path):
        pass

    @staticmethod
    def make_from_file_in_memory(image_data: FileStorage):
        pass

class VideoFactory:
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')
    aws_bucket = os.getenv('AWS_BUCKET')
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    s3 = session.client('s3')
    @staticmethod
    def download_file_from_s3(bucket_name, file_key, local_file_path):
        try:
            VideoFactory.s3.download_file(bucket_name, file_key, local_file_path)
            print(f"File {file_key} downloaded successfully as {local_file_path}")
        except Exception as e:
            print(f"Error downloading file {file_key}: {e}")

    @staticmethod
    def make_from_url(video_url):
        temp_dir = tempfile.gettempdir()

        if video_url.startswith("http"):
            temp_url = video_url.split("?")[0]
            file_name = temp_url.split("/")[-1] + ".mp4"
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading video from URL")
                wget.download(video_url, out=file_path)
                print("Video downloaded")
            except Exception as e:
                print("Error downloading video:", e)
                raise Exception("Error Downloading Video")
        else:
            bucket_name = VideoFactory.aws_bucket
            file_key = video_url
            file_name = file_key.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading video from S3")
                VideoFactory.download_file_from_s3(bucket_name, file_key, file_path)
                print("Video downloaded")
            except Exception as e:
                print("Error downloading video from S3:", e)
                raise Exception("Error Downloading Video")

        return {"path": file_path}

    @staticmethod
    def make_from_file_on_disk(video_path):
        return {"path": video_path}

    @staticmethod
    def make_from_file_in_memory(file_data: FileStorage):
        # save on disk
        fname = tempfile.gettempdir() + os.sep + file_data.filename
        file_data.save(fname)
        return {"path": fname}


class AudioFactory:
    @staticmethod
    def make_from_url(audio_url):
        temp_dir = tempfile.gettempdir()
        temp_url = audio_url.split("?")[0]
        file_name = temp_url.split("/")[-1] + ".wav"
        audio_file = temp_dir + os.sep + file_name
        try:
            print("Downloading audio from url")
            wget.download(audio_url, out=audio_file)
            print("audio downloaded")
        except Exception as e:
            log.exception("Error downloading audio:", e)
            raise Exception("Error Downloading audio")
        return {"path": audio_file}

    @staticmethod
    def make_from_file_on_disk(audio_path):
        return {"path": audio_path}


media_factory = {
    MediaType.TEXT: TextFactory,
    MediaType.IMAGE: ImageFactory,
    MediaType.VIDEO: VideoFactory,
    MediaType.AUDIO: AudioFactory,
}
