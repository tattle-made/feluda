import boto3
import os

class AWSS3Utils:
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
            AWSS3Utils.s3.download_file(bucket_name, file_key, local_file_path)
            print(f"File {file_key} downloaded successfully!")
        except Exception as e:
            print(f"Error downloading file {file_key}: {e}")
            raise Exception("Error Downloading file from S3")