"""
Module to handle read / write from / to S3.
"""

import json
from typing import List, Dict
import boto3


def get_url_video_s3(bucket, key):
    """Returns a URL for a file stored in s3://bucket/key"""
    s3_client = boto3.client("s3")
    url = s3_client.generate_presigned_url("get_object",
                                           Params={"Bucket": bucket, "Key": key},
                                           ExpiresIn=3600)
    return url


def save_json(data: List[Dict], path_to_json: str):
    """Save data to JSON.
    data: Output of pose estimation pipeline to save.
    path_to_json: Path to save
    """
    with open(path_to_json, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def write_json_to_s3(data, bucket, key):
    """Writes a JSON data to s3://bucket/key"""
    s3 = boto3.client("s3")
    s3.put_object(
        Body=json.dumps(data),
        Bucket=bucket,
        Key=key
    )
