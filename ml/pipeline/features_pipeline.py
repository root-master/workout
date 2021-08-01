"""
run inferece pipeline on local.
run ml/pipeline/features_pipeline.py
"""
import json
from typing import List, Dict
import time

import numpy
import cv2
import boto3

from ml.features.pose_estimation.inference_2d.inference_detectron2 import Detectron2_Predictor
from ml.features.pose_estimation.inference_3d.inference_VideoPose3d import VideoPose3d_coco_predictor


def read_video(path_to_video: str,
               frame_start: int = None,
               frame_end: int = None) -> List[numpy.ndarray]:
    """Reads video from a local path or a url.

    Args:
        path_to_video: A path or a url to a video.
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


def get_url_video_s3(bucket, key):
    s3_client = boto3.client("s3")
    url = s3_client.generate_presigned_url("get_object",
                                           Params={"Bucket": bucket, "Key": key},
                                           ExpiresIn=600)  # this url will be available for 600 seconds
    return url


def save_json(data: List[Dict], path_to_json: str):
    """Save data to JSON.
    data: Output of pose estimation pipeline to save.
    path_to_json: Path to save
    """
    with open(path_to_json, "w") as f:
        json.dump(data, f, sort_keys=True, indent=4)


def process_to_json(list_of_pose_features_dict, keypoints_2d, keypoints_3d):
    """Add 3d keypoints and convert numpy arrays to list."""
    for i in range(len(list_of_pose_features_dict)):
        del list_of_pose_features_dict[i]["pred_keypoint_heatmaps"]
        list_of_pose_features_dict[i]["pred_keypoint_2d"] = keypoints_2d[i]
        list_of_pose_features_dict[i]["pred_keypoint_3d"] = keypoints_3d[i]
        for k, v in list_of_pose_features_dict[i].items():
            if isinstance(v, numpy.ndarray):
                list_of_pose_features_dict[i][k] = v.tolist()
    return list_of_pose_features_dict


def write_json_to_s3(data, bucket, key):
    s3 = boto3.client("s3")
    s3.put_object(
        Body=json.dumps(data),
        Bucket=bucket,
        Key=key
    )


def run(source: str,
        bucket: str = None,
        video_path_s3: str = None,
        path_to_video_local: str = None,
        path_to_json: str = None,
        frame_start: int = None,
        frame_end: int = None):
    """Runs the pose estimation pipeline in local.
    video_source: ["local", "s3"]
    """
    if source == "s3":
        path_to_video = get_url_video_s3(bucket, video_path_s3)
    else:
        path_to_video = path_to_video_local
    start = time.time()
    list_of_frames = read_video(path_to_video, frame_start, frame_end)
    print("1. reading video. Time elapsed = ", int(time.time() - start))
    print("length of video is ", len(list_of_frames), " frames")

    start_2d = time.time()
    inference_2d_predictor = Detectron2_Predictor()
    list_of_pose_features_dict = inference_2d_predictor.run_on_video(list_of_frames)
    print("2. running 2d pose estimation on frames. Time elapsed = ", int(time.time() - start_2d))

    start_3d = time.time()
    inference_3d_predictor = VideoPose3d_coco_predictor()
    keypoints_2d, keypoints_2d_normalized = \
        inference_3d_predictor.extract_keypoints_from_detectron2_output(list_of_pose_features_dict)
    print("3. running 3d pose estimation on frames. Time elapsed = ", int(time.time() - start_3d))
    keypoints_3d = inference_3d_predictor.infer3d(keypoints_2d_normalized)
    list_of_pose_features_dict = process_to_json(list_of_pose_features_dict, keypoints_2d, keypoints_3d)

    if source == "s3":
        if path_to_json:
            write_json_to_s3(list_of_pose_features_dict, bucket, path_to_json)
        else:
            save_json(list_of_pose_features_dict, path_to_json)

    return list_of_pose_features_dict


def main():
    pass


# run(source="s3",
#     bucket="workout-vision",
#     video_path_s3="data/workout/squat/video/from_1612153353.520448_to_1612153358.573516.avi",
#     path_to_json="data/workout/squat/features/from_1612153353.520448_to_1612153358.573516.json"
#     )
#
# run(source="s3",
#     bucket="workout-vision",
#     video_path_s3="data/workout/squat/video/from_1612153367.809179_to_1612153372.837415.avi",
#     path_to_json="data/workout/squat/features/from_1612153367.809179_to_1612153372.837415.json"
#     )
run(source="s3",
    bucket="workout-vision",
    video_path_s3="data/workout/clean/Clean-Ty14ogq_Vok.mp4",
    path_to_json="data/workout/clean/Clean-Ty14ogq_Vok.json"
    )

