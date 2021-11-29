from features.pipeline import features_pipeline

movement_list = ["v-ups", "squat", "rowing", "push-up", "kettlebell-russian-swing", "hang-clean", "dead-lift"]

video_name_list = ["train_squat_QifjltKUMCk.mp4",
                   "train_squat_mGvzVjuY8SY.mp4",
                   "test_squat_jacobrafati_set_1.mov",
                   "test_squat_jacobrafati_set_2.mov",
                   "test_squat_jacobrafati_set_3.mov"]

for video_name in video_name_list:
    feature_file_name = video_name[:-4] + ".json"
    # features_pipeline.run(source="s3",
    #                       bucket="workout-vision",
    #                       video_path_s3=f"prototype/video/{video_name}",
    #                       path_to_json=f"prototype/features/{feature_file_name}"
    #                       )

    features_pipeline.run(video_source="local",
                          bucket="workout-vision",
                          video_path=f"./data/prototype/video/{video_name}",
                          features_source="s3",
                          features_path=f"prototype/features/{feature_file_name}"
                          )
