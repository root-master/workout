"""
Module for video utils.
"""

from typing import List

import numpy
import cv2


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


def write(list_of_frames: List[numpy.ndarray],
          path_to_video: str,
          width: int,
          height: int,
          fps: int = 30,
          frame_start: int = None,
          frame_end: int = None):
    out = cv2.VideoWriter(path_to_video,
                          cv2.VideoWriter_fourcc("M", "J", "P", "G"),
                          fps,
                          (width, height))
    for i, frame in enumerate(list_of_frames):
        if frame_start and i < frame_start:
            continue
        if frame_end and i > frame_end:
            break
        out.write(frame)
    out.release()
