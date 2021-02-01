"""
Capture from camera or video file.
"""
from datetime import datetime
from queue import Queue

import cv2
import pytz

from workout.video.writer import Writer


def now():
    return datetime.now().astimezone(pytz.timezone("US/Pacific")).timestamp()


class Capture(object):
    """Video capturing from a camera or a video file."""

    def __init__(self,
                 source,
                 end_time: int = None,
                 queue_max_size: int = 0,
                 video_writer: Writer = None):
        """Initializes video capturing form a camera source or a video file.

        Args:
            source: A camera source (int) or a file_path (str).
            end_time: The capturing loop ends after end_time (in seconds). It releases cv2.VideoCapture.
                if end_time = None, the loop runs forever.
        """
        self.time_stamp_list = []
        self.end_time = end_time
        self.source = source
        self.frame_number = 0
        # json is to store the captured frames in RAM
        self.timestamp_frames_dict = {}  # key=timestamp, value=frame
        self.name = "capture"
        # Q is a Queue of keys (timestamp of captured frames)
        self.queue_max_size = queue_max_size
        self.height, self.width = None, None
        self.timestamp_queues = Queue(maxsize=self.queue_max_size)
        self.video_writer = video_writer

        self.reset()

    def reset(self):
        self.video = cv2.VideoCapture(self.source)
        self.frame_number = 0
        self.stopped = False
        success, frame = self.video.read()
        if success:
            self.height, self.width = frame.shape[:2]

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            self.stop()

        timestamp = now()
        self.frame_number += 1
        self.time_stamp_list.append(timestamp)  # save timestamp
        self.timestamp_queues.put(timestamp)  # push timestamp to a Queue
        self.timestamp_frames_dict[timestamp] = frame  # key: timestamp, value: frame
        self.end_timestamp = timestamp
        self.frame = frame
        self.success = success

    def capture(self, write=False):
        """Capture loop."""
        self.start_timestamp = now()
        while True:
            if self.verify_stop_cond():
                self.stop()
                return

            # otherwise, read the next frame from the stream
            self.get_frame()
            self.elapsed_time = now() - self.start_timestamp
            # print("captured frame {frame} -- timestamp {timestamp}".format(frame=self.frame_number,
            #                                                                timestamp=self.elapsed_time))

            if write:
                self.write()

    def verify_stop_cond(self):
        """Verifies capture loop condition."""
        if self.stopped:
            return True
        if self.end_time is not None and self.elapsed() >= self.end_time:
            return True
        if not self.video.isOpened():
            return True

        return False

    def write(self):
        if self.video_writer is None:
            raise TypeError("video_writer (a Writer instance) should be initiated and passed to Capture.")
        self.video_writer.write(self.frame)

    def elapsed(self):
        return now() - self.start_timestamp

    def fps(self):
        return self.frame_number / self.elapsed_time

    def stop(self):
        self.__del__()

    def __del__(self):
        self.stopped = True
        self.video.release()
        if self.video_writer is not None:
            self.video_writer.stop()
