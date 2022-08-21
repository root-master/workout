import mediapipe as mp
import cv2
import json
from typing import List, Dict
import boto3
import numpy
import cv2


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


def read(path_to_video: str,
         frame_start: int = None,
         frame_end: int = None) -> List[numpy.ndarray]:
    """Reads a video frames from a local path or a URL.

    Args:
        path_to_video: A path or a url to a utils.
        frame_start: Starting frame
        frame_end: End frame.

    Returns: a list of frame images.
    """
    cap = cv2.VideoCapture(path_to_video)
    counter = 0
    list_of_frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        counter += 1
        if frame_start and counter < frame_start:
            continue
        if frame_end and counter >= frame_end:
            break
        if ret:
            list_of_frames.append(frame)
        else:
            break
    cap.release()
    return list_of_frames


test_video_url = get_url_video_s3(bucket="workout-vision-public",
                                  key="user_videos/yrafati/1653674011763_1653674202014.mp4")
test_video_frames = read(path_to_video=test_video_url)

train_video_url = get_url_video_s3(bucket="workout-vision-public",
                                   key="training_videos/train_standing_pose_ifIbl3wMNog.mp4")
train_video_frames = read(path_to_video=train_video_url)
