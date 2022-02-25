"""
Module for downloading utils from Youtube.
"""

import os
from typing import List
import youtube_dl

os.system("echo Hello from the other side!")


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d["status"] == "finished":
        print("Done downloading, now converting ...")


# ydl_opts = {
#     "format": "bestaudio/best",
#     "postprocessors": [{
#         "key": "FFmpegExtractAudio",
#         "preferredcodec": "mp3",
#         "preferredquality": "192",
#     }],
#     "logger": MyLogger(),
#     "progress_hooks": [my_hook],
# }

ydl_opts = {}


def download_youtube_video(url_list: List[str]):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(url_list)


def download_portion_of_youtube_video(video_url, start_time, end_time, download_file_name):
    command = """ffmpeg $(youtube-dl -g '{video_url}' | sed "s/.*/-ss 
    {start_time} -i &/") -t {end_time} -c copy {download_file_name}"""
    command = command.format(video_url=video_url, start_time=start_time,
                             end_time=end_time, download_file_name=download_file_name)
    os.system(command)


# download_youtube_video(["https://www.youtube.com/watch?v=QifjltKUMCk"])
# download_portion_of_youtube_video(video_url="https://www.youtube.com/watch?v=QifjltKUMCk",
#                                   start_time=37,
#                                   end_time=18,
#                                   download_file_name="squat.mkv")
#
# download_portion_of_youtube_video(video_url="https://www.youtube.com/watch?v=QifjltKUMCk",
#                                   start_time=37,
#                                   end_time=18,
#                                   download_file_name="squat.mkv")
