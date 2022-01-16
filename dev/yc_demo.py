from features.pipeline import pose_estimation_pipeline

movement_list = ["v-ups", "squat", "rowing", "push-up", "kettlebell-russian-swing", "hang-clean", "dead-lift"]

for movement in movement_list:
    video_file_name = movement + ".mov"
    feature_file_name = movement + ".json"
    print(f"yc-demo/video/{video_file_name}")
    # features_pipeline.run(video_source="s3",
    #                       bucket="workout-vision",
    #                       video_path_s3=f"yc-demo/video/{video_file_name}",
    #                       features_source="s3",
    #                       features_path=f"yc-demo/features/{video_file_name}"
    #                       )
