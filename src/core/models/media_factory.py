import requests
from requests.exceptions import ConnectTimeout
import PIL
from io import BytesIO
import numpy as np
from werkzeug.datastructures import FileStorage
import wget
from core.models.media import MediaType
from core.models.s3_utils import AWSS3Utils
import logging
import os
import tempfile
from pydub import AudioSegment

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
    def make_from_url_to_path(image_url):
        
        temp_dir = tempfile.gettempdir()
        temp_url = image_url.split("?")[0]
        file_name = temp_url.split("/")[-1]
        image_path = os.path.join(temp_dir, file_name)
        try:
            print("Downloading image from URL")
            wget.download(image_url, out=image_path)
            print("\nImage downloaded")
        except Exception as e:
            print("Error downloading image:", e)
            raise Exception("Error Downloading Image")
        return {"path": image_path}


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
                print("\nVideo downloaded")
            except Exception as e:
                print("Error downloading video:", e)
                raise Exception("Error Downloading Video")
        else:
            bucket_name = AWSS3Utils.aws_bucket
            file_key = video_url
            file_name = file_key.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading video from S3")
                AWSS3Utils.download_file_from_s3(bucket_name, file_key, file_path)
                print("\nVideo downloaded")
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

        if audio_url.startswith("http"):
            temp_url = audio_url.split("?")[0]
            file_name = temp_url.split("/")[-1] + ".wav"
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading audio from URL")
                wget.download(audio_url, out=file_path)
                print("\nAudio downloaded")
            except Exception as e:
                print("Error downloading audio:", e)
                raise Exception("Error Downloading audio")
        else:
            bucket_name = AWSS3Utils.aws_bucket
            file_key = audio_url
            file_name = file_key.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading audio from S3")
                AWSS3Utils.download_file_from_s3(bucket_name, file_key, file_path)
                print("\nAudio downloaded")
            except Exception as e:
                print("Error downloading audio from S3:", e)
                raise Exception("Error Downloading audio")

        return {"path": file_path}

    @staticmethod
    def make_from_url_to_wav(audio_url):
        temp_dir = tempfile.gettempdir()
        temp_url = audio_url.split("?")[0]
        file_name = temp_url.split("/")[-1]
        audio_file = os.path.join(temp_dir, file_name)

        try:
            print("Downloading audio from URL")
            wget.download(audio_url, out=audio_file)
            print("\naudio downloaded")

            _, file_extension = os.path.splitext(file_name)
            if file_extension != '.wav':
                audio = AudioSegment.from_file(audio_file, format=file_extension[1:])
                wav_file = os.path.splitext(audio_file)[0] + '.wav'
                audio.export(wav_file, format='wav')
                os.remove(audio_file)
                audio_file = wav_file
        except Exception as e:
            logging.exception("Error downloading or converting audio:", e)
            raise Exception("Error downloading or converting audio")
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
