from google.cloud import vision
import json, os
import boto3
from google.protobuf.json_format import MessageToJson
import PIL
from io import BytesIO
from image_analyzer import ResNet18
from datetime import datetime
from text import detect_lang
from monitor import timeit
import requests
import np

resnet18 = ResNet18()


def get_credentials():
    """
    Conditionally downloads Google Credentials to be used by
    Cloud Vision API.
    """
    # check if credentials are available locally
    if os.path.exists("credentials.json"):
        print("file exists. not doing anything")
    else:
        print("downloading credentials")
        aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY_ID")
        bucket = os.environ.get("AWS_BUCKET")
        obj = os.environ.get("S3_CREDENTIALS_PATH")
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        s3.download_file(bucket, obj, "credentials.json")
        print("credentials downloaded")


GOOGLE_API_KEY = get_credentials()


def detect_text(img_bytes):
    client = vision.ImageAnnotatorClient()
    image_data = vision.types.Image(content=img_bytes)
    resp = client.text_detection(image=image_data)
    resp = json.loads(MessageToJson(resp))
    text = resp.get("fullTextAnnotation", {}).get("text", "")
    return {"text": text, "full": resp}


def get_vector_from_file(file):
    image_bytes = file.read()
    image = PIL.Image.open(BytesIO(image_bytes))
    image_vec = resnet18.extract_feature(image)
    return image_vec


@timeit
def image_from_url(image_url):
    resp = requests.get(image_url)
    image_bytes = resp.content
    image = PIL.Image.open(BytesIO(image_bytes))
    image_array = np.array(image)
    return {"image": image, "image_array": image_array, "image_bytes": image_bytes}


def get_vector_from_url(url):
    image_dict = image_from_url(url)
    image = image_dict["image"]
    image = image.convert("RGB")  # take care of png(RGBA) issue
    image_vec = resnet18.extract_feature(image)
    return image_vec


def get_vector(source, type="url"):
    """
    source could be a url or a wertrezeug.File object containing the raw
    bytes of the file.
    """
    if type == "url":
        return get_vector_from_url(source)
    elif type == "file":
        return get_vector_from_file(source)
    else:
        raise "Unexpected image source."


def get_doc(source, data, featureFlags, type):
    """
    source could be a url or a wertrezeug.File object containing the raw
    bytes of the file.
    """
    doc = {}

    image_vec = get_vector(source, type)
    date = datetime.utcnow()

    if featureFlags.include_text_vector:
        detected_text = detect_text(image_bytes).get("text", "")
        lang = detect_lang(detected_text)
        has_text, text_vec = get_vector(detect_text, lang)

        doc["text"] = detected_text
        doc["text_vec"] = text_vec
        doc["lang"] = lang
        doc["has_text"] = has_text
    elif featureFlags.include_composite_vector:
        combined_vec = np.hstack((image_vec, text_vec)).tolist()
        doc["combined_vec"] = combined_vec

    doc["date_added"] = date
    doc["image_vec"] = image_vec

    return doc
