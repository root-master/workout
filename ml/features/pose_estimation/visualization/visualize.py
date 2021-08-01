"""
Visualization tools.
run ml/features/pose_estimation/visualization/visualize.py
"""
import json
from typing import List

import cv2
import numpy

from ml.features.pose_estimation.inference_3d.utils import image_coordinates, camera_to_world


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

video = read_video("data/workout/squat/video/from_1612153353.520448_to_1612153358.573516.avi")
data = load_json("data/workout/squat/test.json")

i = 10
image = video[i]
width = data[i]["image"]["width"]
height = data[i]["image"]["height"]
keypoint_2d = numpy.array(data[i]["pred_keypoint_2d"])
keypoint_3d = numpy.array(data[i]["pred_keypoint_3d"])
rot = custom_camera_params["orientation"]
prediction_rot = camera_to_world(keypoint_3d, R=rot, t=0)
prediction_rot[:, 2] -= numpy.min(keypoint_3d[:, 2])

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
xs = prediction_rot[:, 0]
ys = prediction_rot[:, 1]
zs = prediction_rot[:, 2]
ax.plot3D(xs, ys, zs, '.')
plt.show()
