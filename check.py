import os
import botocore
import boto3
from botocore.exceptions import ClientError
from config import aws_access_key_id, aws_secret_access_key, region_name, bucket_name


def check_bucket_exists(bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name)
    try:
        s3.head_bucket(Bucket=bucket_name)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise


def check_file_exists(bucket_name, object_name):
    s3 = boto3.resource('s3',
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=object_name):
        if obj.key == object_name:
            return True
    return False


def upload_file(file_path, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_path: Path to the file to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, False if file already exists or upload failed
    """

    # If S3 object_name was not specified, use file_path basename
    if object_name is None:
        object_name = os.path.basename(file_path)


    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)
    try:
        response = s3_client.upload_file(file_path, bucket, object_name)
        return True
    except ClientError as e:
        print(f"Failed to upload file '{object_name}': {e}")
        return False