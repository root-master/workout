"""
Visualization tools.
run ml/features/pose_estimation/visualization/visualize.py
"""
import json
from typing import List

import cv2
import numpy

from features.pose_estimation.inference_3d.skeleton import Skeleton
from features.pose_estimation.inference_3d.utils import camera_to_world
from features.visualization.visualization import render_animation


def load_json(path_to_json: str):
    with open(path_to_json) as f:
        data = json.load(f)
    return data


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


custom_camera_params = {
    'id': None,
    'res_w': None,  # Pulled from metadata
    'res_h': None,  # Pulled from metadata

    # Dummy camera parameters (taken from Human3.6M), only for visualization purposes
    'azimuth': 70,  # Only used for visualization
    'orientation': [0.1407056450843811, -0.1500701755285263, -0.755240797996521, 0.6223280429840088],
    'translation': [1841.1070556640625, 4955.28466796875, 1563.4454345703125],
}

coco_keypoints_mapping_dict = {
    0: "nose",
    1: "left_eye",
    2: "right_eye",
    3: "left_ear",
    4: "right_ear",
    5: "left_shoulder",
    6: "right_shoulder",
    7: "left_elbow",
    8: "right_elbow",
    9: "left_wrist",
    10: "right_wrist",
    11: "left_hip",
    12: "right_hip",
    13: "left_knee",
    14: "right_knee",
    15: "left_ankle",
    16: "right_ankle"
}

lines = [[0, 1], [0, 2], [1, 3], [2, 4],
         [5, 6], [5, 7], [6, 8], [7, 9], [8, 10],
         [11, 12], [11, 13], [12, 14], [13, 15], [14, 16]]

bucket = "workout-vision"
video_path = "data/prototype/video/test_squat_jacobrafati_set_3.mov"
path_to_json = "data/prototype/features/test_squat_jacobrafati_set_3.json"

video = read_video(video_path)
data = load_json(path_to_json)

keypoint_2d_all = numpy.zeros((len(data), 17, 2))
keypoint_3d_all = numpy.zeros((len(data), 17, 3))

width = data[0]["image"]["width"]
height = data[0]["image"]["height"]

custom_camera_params['res_w'] = width
custom_camera_params['res_h'] = height

for i, image in enumerate(data):
    keypoint_2d = numpy.array(data[i]["pred_keypoint_2d"])
    keypoint_3d = numpy.array(data[i]["pred_keypoint_3d"])
    keypoint_2d_all[i, :, :] = keypoint_2d
    keypoint_3d_all[i, :, :] = keypoint_3d

keypoints_metadata = {'layout_name': 'coco',
                      'num_joints': 17,
                      'keypoints_symmetry': [[1, 3, 5, 7, 9, 11, 13, 15],
                                             [2, 4, 6, 8, 10, 12, 14, 16]],
                      'video_metadata': {'squat_short': {'w': width, 'h': height}}}

rot = custom_camera_params["orientation"]
prediction_rot = camera_to_world(keypoint_3d_all, R=rot, t=0)
# prediction_rot[:, :, 2] -= numpy.min(prediction_rot[:, :, 2])
prediction_rot[:, :, 2] -= numpy.min(prediction_rot[:, :, 2], axis=1, keepdims=True)

# prediction_rot[:, :, 2] -= prediction_rot[:, 3, 2]

keypoints = keypoint_2d_all
poses = {'Reconstruction': prediction_rot}
skeleton = Skeleton(parents=numpy.array([-1, 0, 1, 2, 0, 4, 5, 0, 7, 8, 9, 8, 11, 12, 8, 14, 15]),
                    joints_left=numpy.array([4, 5, 6, 11, 12, 13]),
                    joints_right=numpy.array([1, 2, 3, 14, 15, 16]))
fps = 30
bitrate = 3000
azim = custom_camera_params['azimuth']
output = "data/prototype/output_videos/test_squat_jacobrafati_set_3_3d.mp4"
viewport = (custom_camera_params['res_w'], custom_camera_params['res_h'])
input_video_path = video_path

render_animation(keypoints, keypoints_metadata, poses, skeleton, fps, bitrate, azim, output,
                             viewport, limit=-1, downsample=1, size=6, input_video_path=input_video_path,
                             input_video_skip=0)

# """
# Visualization tools.
# run ml/features/pose_estimation/visualization/visualize.py
# """
# import json
# from typing import List
#
# import boto3
# import cv2
# import numpy
#
# from features.pose_estimation.inference_3d.skeleton import Skeleton
# from features.pose_estimation.inference_3d.utils import camera_to_world
# from features.visualization.visualization import render_animation
#
#
# def load_json(path_to_json: str):
#     with open(path_to_json) as f:
#         data = json.load(f)
#     return data
#
#
# def read_video(path_to_video: str,
#                frame_start: int = None,
#                frame_end: int = None) -> List[numpy.ndarray]:
#     """Reads video from a local path or a url.
#
#     Args:
#         path_to_video: A path or a url to a video.
#         frame_start: Starting frame
#         frame_end: End frame.
#
#     Returns: a list of frame images.
#     """
#     cap = cv2.VideoCapture(path_to_video)
#     counter = 0
#     list_of_frames = []
#     while cap.isOpened():
#         ret, frame = cap.read()
#         counter += 1
#         if frame_start and counter < frame_start:
#             continue
#         if frame_end and counter >= frame_end:
#             break
#         if ret:
#             list_of_frames.append(frame)
#         else:
#             break
#     cap.release()
#     return list_of_frames
#
#
# def get_json_from_s3(bucket, key):
#     s3 = boto3.resource('s3')
#     obj = s3.Object(bucket, key)
#     data = json.load(obj.get()['Body'])
#     return data
#
#
# custom_camera_params = {
#     'id': None,
#     'res_w': None,  # Pulled from metadata
#     'res_h': None,  # Pulled from metadata
#
#     # Dummy camera parameters (taken from Human3.6M), only for visualization purposes
#     'azimuth': 70,  # Only used for visualization
#     'orientation': [0.1407056450843811, -0.1500701755285263, -0.755240797996521, 0.6223280429840088],
#     'translation': [1841.1070556640625, 4955.28466796875, 1563.4454345703125],
# }
#
# coco_keypoints_mapping_dict = {
#     0: "nose",
#     1: "left_eye",
#     2: "right_eye",
#     3: "left_ear",
#     4: "right_ear",
#     5: "left_shoulder",
#     6: "right_shoulder",
#     7: "left_elbow",
#     8: "right_elbow",
#     9: "left_wrist",
#     10: "right_wrist",
#     11: "left_hip",
#     12: "right_hip",
#     13: "left_knee",
#     14: "right_knee",
#     15: "left_ankle",
#     16: "right_ankle"
# }
#
# lines = [[0, 1], [0, 2], [1, 3], [2, 4],
#          [5, 6], [5, 7], [6, 8], [7, 9], [8, 10],
#          [11, 12], [11, 13], [12, 14], [13, 15], [14, 16]]
#
# bucket = "workout-vision"
# video_path_s3 = "data/workout/clean/video/Clean-Ty14ogq_Vok_1.mp4"
# path_to_json = "data/workout/clean/features/Clean-Ty14ogq_Vok_1.json"
#
# video = read_video(video_path_s3)
# key = path_to_json
#
# data = get_json_from_s3(bucket, key)
#
# # for d in data:
# #     for key in d.keys():
# #         if "pred" in key:
# #             d[key] = numpy.array(d[key])
#
# # data_3d_videopose3d = numpy.load("data/workout/squat/features/features_3d_from_1612153353.520448_to_1612153358.573516.npz.npy")
# # data_pp_past = numpy.load("data/workout/squat/features/features_2d_pp_from_1612153353.520448_to_1612153358.573516.npz")
#
# keypoint_2d_all = numpy.zeros((len(data), 17, 2))
# keypoint_3d_all = numpy.zeros((len(data), 17, 3))
#
# width = data[0]["image"]["width"]
# height = data[0]["image"]["height"]
#
# custom_camera_params['res_w'] = width
# custom_camera_params['res_h'] = height
#
# for i, image in enumerate(data):
#     keypoint_2d = numpy.array(data[i]["pred_keypoint_2d"])
#     keypoint_3d = numpy.array(data[i]["pred_keypoint_3d"])
#     keypoint_2d_all[i, :, :] = keypoint_2d
#     keypoint_3d_all[i, :, :] = keypoint_3d
#
# keypoints_metadata = {'layout_name': 'coco',
#                       'num_joints': 17,
#                       'keypoints_symmetry': [[1, 3, 5, 7, 9, 11, 13, 15],
#                                              [2, 4, 6, 8, 10, 12, 14, 16]],
#                       'video_metadata': {'squat_short': {'w': width, 'h': height}}}
#
# rot = custom_camera_params["orientation"]
# prediction_rot = camera_to_world(keypoint_3d_all, R=rot, t=0)
# # prediction_rot[:, :, 2] -= numpy.min(prediction_rot[:, :, 2])
# prediction_rot[:, :, 2] -= numpy.min(prediction_rot[:, :, 2], axis=1, keepdims=True)
#
# # prediction_rot[:, :, 2] -= prediction_rot[:, 3, 2]
#
# keypoints = keypoint_2d_all
# poses = {'Reconstruction': prediction_rot}
# skeleton = Skeleton(parents=numpy.array([-1, 0, 1, 2, 0, 4, 5, 0, 7, 8, 9, 8, 11, 12, 8, 14, 15]),
#                     joints_left=numpy.array([4, 5, 6, 11, 12, 13]),
#                     joints_right=numpy.array([1, 2, 3, 14, 15, 16]))
# fps = 30
# bitrate = 3000
# azim = custom_camera_params['azimuth']
# output = "data/workout/clean/output/Clean-Ty14ogq_Vok_1.mp4"
# viewport = (custom_camera_params['res_w'], custom_camera_params['res_h'])
# input_video_path = video_path_s3
#
# render_animation(keypoints, keypoints_metadata, poses, skeleton, fps, bitrate, azim, output,
#                  viewport, limit=-1, downsample=1, size=6, input_video_path=input_video_path,
#                  input_video_skip=0)
#
# center_hip = 0
# left_hip = 1
# left_knee = 2
# left_ankle = 3
# right_hip = 4
# right_knee = 5
# right_ankle = 6
# mid_section = 7
# neck = 8
# nose = 9
# head = 10
# right_shoulder = 11
# right_elbow = 12
# right_hand = 13
# left_shoulder = 14
# left_elbow = 15
# left_hand = 16
#
# # image = video[i]
# # width = data[i]["image"]["width"]
# # height = data[i]["image"]["height"]
# # keypoint_2d = numpy.array(data[i]["pred_keypoint_2d"])
#
# # import matplotlib.pyplot as plt
# #
# # fig = plt.figure()
# # plt.imshow(image[..., ::-1])
# # plt.plot(keypoint_2d[:, 0], keypoint_2d[:, 1], 'o')
# # for line in lines:
# #     i, j = line[0], line[1]
# #     x1, y1 = keypoint_2d[i, 0], keypoint_2d[i, 1]
# #     x2, y2 = keypoint_2d[j, 0], keypoint_2d[j, 1]
# #     plt.plot([x1, x2], [y1, y2], '-')
# #
# # # plt.show()
# #
#
# # i = 50
# # keypoint_3d = numpy.array(data[i]["pred_keypoint_3d"])
# # rot = custom_camera_params["orientation"]
# # prediction_rot = camera_to_world(keypoint_3d, R=rot, t=0)
# # prediction_rot[:, 2] -= numpy.min(keypoint_3d[:, 2])
# #
# # import matplotlib.pyplot as plt
# #
# # fig = plt.figure()
# # ax = fig.add_subplot(projection="3d")
# # xs = keypoint_3d[:, 0]
# # ys = keypoint_3d[:, 1]
# # zs = keypoint_3d[:, 2]
# # ax.plot3D(xs, ys, zs, 'o')
# # # for line in lines:
# # #     i, j = line[0], line[1]
# # #     x1, y1, z1 = keypoint_3d[i, 0], keypoint_3d[i, 1], keypoint_3d[i, 2]
# # #     x2, y2, z2 = keypoint_3d[j, 0], keypoint_3d[j, 1], keypoint_3d[j, 2]
# # #     ax.plot3D([x1, x2], [y1, y2], [z1, z2], '-')
# # plt.show()
