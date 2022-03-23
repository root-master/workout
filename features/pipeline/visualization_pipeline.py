"""
Runs visualization after extracting the pose data.
"""
import os
from matplotlib.animation import writers

from features.utils.s3 import upload_file_to_s3
from features.visualization.user_visualization import create_animation


def run(list_of_frames,
        list_of_pose_features_dict,
        angle_key,
        visualization_s3_bucket,
        visualization_s3_key,
        anim_output_local_path="/tmp/output.mp4",
        fps=25.0,
        ):
    anim = create_animation(list_of_frames,
                            list_of_pose_features_dict,
                            angle_key,
                            show=False)
    Writer = writers["ffmpeg"]
    writer = Writer(fps=fps, metadata={}, bitrate=3000)
    # write animation to a temporary local file
    anim.save(anim_output_local_path, writer=writer)
    # upload the animation video from local to s3
    boto3_response = upload_file_to_s3(anim_output_local_path, visualization_s3_bucket, visualization_s3_key)
    # delete the local file
    if os.path.isfile(anim_output_local_path):
        os.remove(anim_output_local_path)

    return boto3_response
