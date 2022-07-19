"""
Runs inference on videos from local or s3.
"""
import time

import numpy

from features.pose_estimation.inference_2d.inference_detectron2 import Detectron2_Predictor
from features.pose_estimation.inference_3d.inference_VideoPose3d import VideoPose3d_coco_predictor
from features.pose_estimation.inference_3d.utils import camera_to_world
from features.pose_estimation.inference_3d.coco import custom_camera_params
from features.dynamics import invariant_features
from features.utils.s3 import get_url_video_s3, save_json, write_json_to_s3
from features.utils.video import read


def post_process(list_of_pose_features_dict,
                 pred_keypoints_2d,
                 pred_keypoints_3d):
    """Add 3d keypoints and renames keys and deletes extra ones."""
    for frame_number, _ in enumerate(list_of_pose_features_dict):
        list_of_pose_features_dict[frame_number]["frame_number"] = frame_number
        list_of_pose_features_dict[frame_number]["width"] = list_of_pose_features_dict[frame_number]["image"]["width"]
        list_of_pose_features_dict[frame_number]["height"] = list_of_pose_features_dict[frame_number]["image"]["height"]
        list_of_pose_features_dict[frame_number]["pred_keypoints_2d"] = pred_keypoints_2d[frame_number]
        list_of_pose_features_dict[frame_number]["pred_keypoints_3d"] = pred_keypoints_3d[frame_number]
        list_of_pose_features_dict[frame_number]["pred_keypoints_3d_world"] = \
            camera_to_world(numpy.array(pred_keypoints_3d[frame_number]), R=custom_camera_params["orientation"], t=0)
        for key in ["scores", "pred_classes", "pred_keypoints", "image", "pred_keypoint_heatmaps"]:
            del list_of_pose_features_dict[frame_number][key]
    return list_of_pose_features_dict


def process_to_json(list_of_pose_features_dict):
    """Converts numpy arrays to lists."""
    for frame_number, _ in enumerate(list_of_pose_features_dict):
        for k, v in list_of_pose_features_dict[frame_number].items():
            if isinstance(v, numpy.ndarray):
                list_of_pose_features_dict[frame_number][k] = v.tolist()
    return list_of_pose_features_dict


def run(video_source: str = None,
        s3_bucket: str = None,
        s3_video_key: str = None,
        video_local_path: str = None,
        features_source: str = None,
        s3_features_key: str = None,
        features_local_path: str = None,
        frame_start: int = None,
        frame_end: int = None,
        save_features: bool = True):
    """Runs the pose estimation pipeline in local.
    video_source: ["local", "s3"]
    """
    start = time.time()
    print("-" * 60)
    print("1. reading video frames.")
    if video_source == "s3":
        print("""s3://{}/{}""".format(s3_bucket, s3_video_key))
        path_to_video = get_url_video_s3(s3_bucket, s3_video_key)
    elif video_source == "local":  # local
        print(video_local_path)
        path_to_video = video_local_path
    else:
        raise KeyError
    list_of_frames = read(path_to_video, frame_start, frame_end)
    print("video is ", len(list_of_frames), " frames.")
    print("Time elapsed = ", int(time.time() - start))

    print("-" * 60)
    print("2. running 2D pose estimation on frames.")
    start_2d = time.time()
    inference_2d_predictor = Detectron2_Predictor()
    list_of_pose_features_dict = inference_2d_predictor.run_on_video(list_of_frames)
    print("Time elapsed = ", int(time.time() - start_2d))

    print("-" * 60)
    print("3. running 3D pose estimation on 2D Keypoints.")
    start_3d = time.time()
    inference_3d_predictor = VideoPose3d_coco_predictor()
    keypoints_2d, keypoints_2d_normalized = \
        inference_3d_predictor.extract_keypoints_from_detectron2_output(list_of_pose_features_dict)
    print("Time elapsed = ", int(time.time() - start_3d))
    keypoints_3d = inference_3d_predictor.infer3d(keypoints_2d_normalized)

    print("-" * 60)
    print("4. postprocessing 2D and 3D features.")
    list_of_pose_features_dict = post_process(list_of_pose_features_dict, keypoints_2d, keypoints_3d)
    list_of_pose_features_dict = process_to_json(list_of_pose_features_dict)

    print("-" * 60)
    print("5. extracting invariant features on 3D Keypoints.")
    list_of_pose_features_dict = invariant_features.run(list_of_pose_features_dict)

    print("-" * 60)
    print("6. processing features to json.")
    list_of_pose_features_dict = process_to_json(list_of_pose_features_dict)

    if save_features:
        print("-" * 60)
        print("7. writing features json to ", features_source)
        if features_source == "s3":
            print("""s3://{}/{}""".format(s3_bucket, s3_features_key))
            write_json_to_s3(list_of_pose_features_dict, s3_bucket, s3_features_key)
        elif features_source == "local":
            print(features_local_path)
            save_json(list_of_pose_features_dict, features_local_path)
        else:
            raise KeyError
    print("-" * 60)

    return list_of_frames, list_of_pose_features_dict


run(video_source="s3",
    s3_bucket="workout-vision-public",
    s3_video_key="training_videos/tarin_standing_pose_ifIbl3wMNog.mp4",
    video_local_path=None,
    features_source="s3",
    s3_features_key="training_features/tarin_standing_pose_ifIbl3wMNog.json",
    features_local_path=None,
    frame_start=None,
    frame_end=None,
    save_features=True)
