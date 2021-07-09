"""
run inferece pipeline on local.
"""
from typing import List

import numpy
import cv2

from ml.pose_estimation.inference.inference_2d.inference_detectron2 import Detectron2_Prediction
from ml.pose_estimation.inference.inference_3d.inference_VideoPose3d import VideoPose3d_coco_prediction


def read_video(path_to_video: str,
               frame_start: int = None,
               frame_end: int = None) -> List[numpy.ndarray]:
    cap = cv2.VideoCapture(path_to_video)
    counter = 0
    frame_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if frame_start and counter < frame_start:
            continue
        if frame_end and counter >= frame_end:
            break
        if ret:
            frame_list.append(frame)
            counter += 1
        else:
            break
    cap.release()
    return frame_list


video = read_video("data/workout/squat/video/from_1612153353.520448_to_1612153358.573516.avi", frame_end=3)
detectron2_predictor = Detectron2_Prediction()
v = VideoPose3d_coco_prediction()
v.load_model()
v.load_weights()
output_2d = []
for image in video:
    output_numpy = detectron2_predictor.infer2d_to_dict_of_numpy_array(image)
    output_2d.append(output_numpy)
keypoints_2d, keypoints_2d_normalized = v.extract_keypoints_from_detectron2_output(output_2d)
keypoints_3d = v.infer3d(keypoints_2d_normalized)

width = output_2d[0]["image"]["width"]
height = output_2d[0]["image"]["height"]

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
frame = video[0]
# plt.imshow(frame)
xs = keypoints_3d[0][:, 0]
ys = keypoints_3d[0][:, 1]
zs = keypoints_3d[0][:, 2]
ax.plot3D(xs, ys, zs, '.')

plt.show()
