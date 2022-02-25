"""
Runs inference on videos from local or s3.
"""
import json
import time

import numpy
import boto3

from features.pose_estimation.inference_2d.inference_detectron2 import Detectron2_Predictor
from features.pose_estimation.inference_3d.inference_VideoPose3d import VideoPose3d_coco_predictor
from utils.s3 import get_url_video_s3, save_json
from utils.video import read_video


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


def run(video_source: str,
        bucket: str = None,
        video_path: str = None,
        features_source: str = None,
        features_path: str = None,
        frame_start: int = None,
        frame_end: int = None):
    """Runs the pose estimation pipeline in local.
    video_source: ["local", "s3"]
    """
    if video_source == "s3":
        path_to_video = get_url_video_s3(bucket, video_path)
    else:
        path_to_video = video_path
    start = time.time()
    list_of_frames = read_video(path_to_video, frame_start, frame_end)
    print("1. reading utils. Time elapsed = ", int(time.time() - start))
    print("length of utils is ", len(list_of_frames), " frames")

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

    if features_source == "s3":
        if features_path:
            write_json_to_s3(list_of_pose_features_dict, bucket, features_path)
        else:
            save_json(list_of_pose_features_dict, features_path)

    return list_of_pose_features_dict
