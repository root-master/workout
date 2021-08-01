"""
run ml/features/pose_estimation/pipeline/s3.py
"""

import boto3
import cv2



cap = cv2.VideoCapture(url)
counter = 0
list_of_frames = []
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        list_of_frames.append(frame)
    else:
        break
cap.release()
