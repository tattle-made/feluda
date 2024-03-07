"""
This operator uses google cloud API to extract text from an image.
the credentials to use the cloud vision API should be present in a file titled credentials.json
in the root folder. if it isn't present, it can be optionally fetched from an aws s3 bucket.
The AWS credentials to do this need to be set in the environment variables : AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY_ID, AWS_BUCKET, S3_CREDENTIALS_PATH

pip install :
google-cloud==0.34.0
google-cloud-vision==0.34.0
boto3
"""


def download_google_cloud_credentials():
    """
    Conditionally downloads Google Credentials to be used by
    Cloud Vision API.
    caveat : this saves the credential file in the root of the project. Don't expect it in the root folder of the
    operator.
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
    return "KEYS STORED IN credentials.json"


def initialize(param):
    global vision, json, os, boto3, MessageToJson, GOOGLE_API_KEY

    from google.cloud import vision
    import json
    import os
    import boto3
    from google.protobuf.json_format import MessageToJson

    GOOGLE_API_KEY = download_google_cloud_credentials()


def run(image):
    """
    file must be an image file of type abc.File
    """
    client = vision.ImageAnnotatorClient()
    image_data = vision.types.Image(content=image["image_bytes"])
    resp = client.text_detection(image=image_data)
    resp = json.loads(MessageToJson(resp))
    text = resp.get("fullTextAnnotation", {}).get("text", "")
    return {"text": text, "full": resp}


def cleanup(param):
    pass


def state():
    return {
        "label": "Detect Text in Image",
        "key": GOOGLE_API_KEY,
    }
