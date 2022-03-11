import os

import numpy
from sklearn.cluster import KMeans
import cv2

from features.pipeline import pose_estimation_pipeline
from features.dynamics import invariant_features

# video_name_list = ["train_squat_QifjltKUMCk.mp4",
#                    "train_squat_mGvzVjuY8SY.mp4",
#                    "test_squat_jacobrafati_set_1.mov",
#                    "test_squat_jacobrafati_set_2.mov",
#                    "test_squat_jacobrafati_set_3.mov"]

video_name_list = ["train_squat_mGvzVjuY8SY.mp4",
                   "test_squat_jacobrafati_set_3.mov"]


def extract_pose_features():
    for video_name in video_name_list:
        feature_file_name = video_name[:-4] + ".json"
        pose_estimation_pipeline.run(video_source="local",
                                     bucket="workout-vision",
                                     video_path=f"./data/prototype/video/{video_name}",
                                     features_source="s3",
                                     features_path=f"prototype/features/{feature_file_name}"
                                     )


def visualize_2d(video_name, video_dir, output_video_name,
                 output_dir, pose_features_list, fps,
                 color=(0, 255, 0), thickness=8):
    video_path = os.path.join(video_dir, video_name)
    video = pose_estimation_pipeline.read_video(video_path)
    output_video_path = os.path.join(output_dir, output_video_name)
    frame_width = pose_features_list[0]["image"]["width"]
    frame_height = pose_features_list[0]["image"]["height"]
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc("M", "J", "P", "G"), fps,
                          (frame_width, frame_height))
    lines = [[0, 1], [0, 2], [1, 3], [2, 4],
             [5, 6], [5, 7], [6, 8], [7, 9], [8, 10],
             [11, 12], [11, 13], [12, 14], [13, 15], [14, 16]]

    for i, frame in enumerate(video):
        keypoints_2d = numpy.array(pose_features_list[i]["pred_keypoints"][0]).astype(int)
        for line in lines:
            i = line[0]
            j = line[1]
            start_point = tuple(list(keypoints_2d[i, :2]))
            end_point = tuple(list(keypoints_2d[j, :2]))
            frame = cv2.line(frame, start_point, end_point, color, thickness)
        out.write(frame)
    out.release()


def extract_invariant_features(pose_features_path):
    features_list = invariant_features.run(pose_features_path)
    return features_list


def convert_features_to_numpy(features_list, start=None, end=None):
    features_meta = ["angle", "velocity"]
    features_keys = features_list[0]["velocity"].keys()
    if start is None:
        start = 0

    if end is None:
        end = len(features_list)
    x = [[features_list[frame_number][feature_meta][feature_key] for
          feature_meta in features_meta for
          feature_key in features_keys] for frame_number in range(start, end)]
    x = numpy.array(x)
    return x


def fit_Kmeans(x_train, n_clusters=2):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(x_train)
    return kmeans


def get_labels(kmeans, x_test=None):
    if x_test is None:
        return kmeans.labels_
    return kmeans.predict(x_test)


def count_reps(y_pred):
    y_pred = list(y_pred)
    y_pred_simplified = []
    current = None
    for i, e in enumerate(y_pred):
        if e != current:
            current = e
            y_pred_simplified.append(e)

    reps = min(y_pred_simplified.count(1), y_pred_simplified.count(0))
    print("reps = ", reps)
    return reps

# train_pose_features_list = invariant_features.read_json("data/prototype/features/train_squat_mGvzVjuY8SY.json")
# test_pose_features_list = invariant_features.read_json("data/prototype/features/test_squat_jacobrafati_set_3.json")
#
# train_features_list = extract_invariant_features("data/prototype/features/train_squat_mGvzVjuY8SY.json")
# test_features_list = extract_invariant_features("data/prototype/features/test_squat_jacobrafati_set_3.json")

# x_train = convert_features_to_numpy(train_features_list)
# x_test = convert_features_to_numpy(test_features_list)
# kmeans = fit_Kmeans(x_train)
# y_train = kmeans.labels_
# y_test = get_labels(kmeans, x_test=x_test)
#
# reps_test = count_reps(y_test)

# visualize_2d(
#     video_name="train_squat_mGvzVjuY8SY.mp4",
#     video_dir="data/prototype/utils/",
#     output_video_name="train_squat_mGvzVjuY8SY_2d.avi",
#     output_dir="data/prototype/output_videos/",
#     fps=30,
#     pose_features_list=train_pose_features_list
# )

# visualize_2d(
#     video_name="test_squat_jacobrafati_set_3.mov",
#     video_dir="data/prototype/utils/",
#     output_video_name="test_squat_jacobrafati_set_3_2d.avi",
#     output_dir="data/prototype/output_videos/",
#     pose_features_list=test_pose_features_list,
#     fps=30,
#     color=(255, 0, 0)
# )
