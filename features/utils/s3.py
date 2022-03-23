"""
Module to handle read / write from / to S3.
"""

import json
from typing import List, Dict
import boto3


def create_boto3_client():
    s3_client = boto3.client("s3",
                             aws_access_key_id="AKIARWDVMH7XZ3GGKCQV",
                             aws_secret_access_key="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",
                             )
    return s3_client


def get_url_video_s3(bucket, key):
    s3_client = create_boto3_client()
    """Returns a URL for a file stored in s3://bucket/key"""
    url = s3_client.generate_presigned_url("get_object",
                                           Params={"Bucket": bucket, "Key": key},
                                           ExpiresIn=3600)
    return url


def save_json(data: List[Dict], path_to_json: str):
    """Save test_data to JSON.
    test_data: Output of pose estimation pipeline to save.
    path_to_json: Path to save
    """
    with open(path_to_json, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def read_json_from_s3(bucket, key):
    s3_client = create_boto3_client()
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response["Body"]
    return json.loads(content.read())


def write_json_to_s3(data, bucket, key):
    """Writes a JSON test_data to s3://bucket/key"""
    s3_client = create_boto3_client()
    s3_client.put_object(
        Body=json.dumps(data),
        Bucket=bucket,
        Key=key
    )


def upload_file_to_s3(file_name, bucket, key):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param key: S3 object name.
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = create_boto3_client()
    response = s3_client.upload_file(file_name, bucket, key)
    return response
