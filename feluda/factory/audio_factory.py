import logging
import os
import tempfile

import wget
from pydub import AudioSegment

from feluda.factory.s3_factory import S3Factory


class AudioFactory:
    @staticmethod
    def make_from_url(audio_url: str) -> dict | None:
        temp_dir = tempfile.gettempdir()

        if audio_url.startswith("http"):
            temp_url = audio_url.split("?", maxsplit=1)[0]
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
            bucket_name = S3Factory.aws_bucket
            file_key = audio_url
            file_name = file_key.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            try:
                print("Downloading audio from S3")
                S3Factory.download_file_from_s3(bucket_name, file_key, file_path)
                print("\nAudio downloaded")
            except Exception as e:
                print("Error downloading audio from S3:", e)
                raise Exception("Error Downloading audio")

        return {"path": file_path}

    @staticmethod
    def make_from_url_to_wav(audio_url: str) -> dict | None:
        temp_dir = tempfile.gettempdir()
        temp_url = audio_url.split("?", maxsplit=1)[0]
        file_name = temp_url.split("/")[-1]
        audio_file = os.path.join(temp_dir, file_name)

        try:
            print("Downloading audio from URL")
            wget.download(audio_url, out=audio_file)
            print("\naudio downloaded")

            _, file_extension = os.path.splitext(file_name)
            if file_extension != ".wav":
                audio = AudioSegment.from_file(audio_file, format=file_extension[1:])
                wav_file = os.path.splitext(audio_file)[0] + ".wav"
                audio.export(wav_file, format="wav")
                os.remove(audio_file)
                audio_file = wav_file
        except Exception as e:
            logging.exception("Error downloading or converting audio:", e)
            raise Exception("Error downloading or converting audio")
        return {"path": audio_file}

    @staticmethod
    def make_from_file_on_disk(audio_path: str) -> dict:
        return {"path": audio_path}
