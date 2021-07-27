"""
run inferece pipeline on local.
run ml/features/pose_estimation/pipeline/local.py
"""
import json
from typing import List, Dict

import numpy
import cv2

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


def run(path_to_video: str,
        path_to_json: str = None,
        frame_start: int = None,
        frame_end: int = None):
    """Runs the pose estimation pipeline in local."""
    list_of_frames = read_video(path_to_video, frame_start, frame_end)
    inference_2d_predictor = Detectron2_Predictor()
    inference_3d_predictor = VideoPose3d_coco_predictor()
    list_of_pose_features_dict = inference_2d_predictor.run_on_video(list_of_frames)
    keypoints_2d, keypoints_2d_normalized = \
        inference_3d_predictor.extract_keypoints_from_detectron2_output(list_of_pose_features_dict)
    keypoints_3d = inference_3d_predictor.infer3d(keypoints_2d_normalized)
    list_of_pose_features_dict = process_to_json(list_of_pose_features_dict, keypoints_2d, keypoints_3d)
    if path_to_json:
        save_json(list_of_pose_features_dict, path_to_json)

    return list_of_pose_features_dict


def main():
    pass
