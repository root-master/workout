"""
Write frames to disk.
"""

import cv2


class Writer(object):
    def __init__(self,
                 path: str,
                 width: int,
                 height: int,
                 fps: float = 30.0,
                 fourcc="MJPG"):
        """Init."""

        self.path = path
        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)
        self.fps = fps
        self.width = width
        self.height = height

        self.video_writer = cv2.VideoWriter(self.path,
                                            self.fourcc,
                                            self.fps,
                                            (self.width, self.height))

    def write(self, frame):
        """Writes frame to writer."""
        self.video_writer.write(frame)

    def write_from_dict(self, timestamp_queues, timestamp_frames_dict):
        """Writes frames from dict to writer."""
        while True:
            if timestamp_queues.empty():
                self.__del__()
                return

            timestamp = timestamp_queues.get()
            frame = timestamp_frames_dict[timestamp]
            self.video_writer.write(frame)

    def stop(self):
        """Stop and delete."""
        self.__del__()

    def __del__(self):
        """Delete and release."""
        self.stopped = True
        self.video_writer.release()
