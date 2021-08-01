from ml.pipeline import run

list_of_pose_features_dict = run(
    path_to_video_local="data/workout/squat/video/from_1612153353.520448_to_1612153358.573516.avi",
    path_to_json="data/workout/squat/test.json",
    frame_end=3)