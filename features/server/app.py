import json

from flask import Flask, jsonify, url_for
from flask import request
from flask_cors import CORS
from celery import Celery
import requests

from features.dynamics.invariant_features import get_angle_key_for_movement
from features.pipeline import features_pipeline
from features.pipeline import visualization_pipeline


def make_celery(app):
    celery_app = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"]
    )
    celery_app.conf.update(app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


flask_app = Flask(__name__)
CORS(flask_app)
flask_app.config.update(
    CELERY_BROKER_URL="redis://localhost:6379",
    CELERY_RESULT_BACKEND="redis://localhost:6379"
)
celery = make_celery(flask_app)


@flask_app.route("/", methods=["GET", "POST", "DELETE"])
def yo():
    return "YO! THIS IS A MESSAGE FROM WORKOUT VISION ML FEATURES SERVER. LOVE YOURSELF!"


@celery.task()
def run_features_pipeline_task(user_session_data):
    print(user_session_data)
    # video_source = request_data["user_video"]["source"]
    user_video_id = user_session_data["user_video_id"]
    video_source = "s3"
    s3_bucket = user_session_data["user_video"]["bucket"]
    s3_video_key = user_session_data["user_video"]["key"]
    features_source = "s3"
    user_nickname = user_session_data["user"]["nickname"]
    time_stamp_start = user_session_data["timestamp_start"]
    time_stamp_end = user_session_data["timestamp_end"]
    s3_features_key = """user_features/{}/{}_{}.json""".format(user_nickname,
                                                               time_stamp_start,
                                                               time_stamp_end)
    print("=" * 60)
    print("-" * 15 + "  FEATURES PIPELINE  " + "-" * 15)
    list_of_frames, list_of_pose_features_dict = features_pipeline.run(video_source=video_source,
                                                                       s3_bucket=s3_bucket,
                                                                       s3_video_key=s3_video_key,
                                                                       features_source=features_source,
                                                                       s3_features_key=s3_features_key)
    user_features_s3_dict = {"key": s3_features_key,
                             "bucket": s3_bucket}
    print("-" * 15 + "  VISUALIZATION PIPELINE  " + "-" * 15)
    movement_name = user_session_data["movement"]["movementName"]
    angle_key = get_angle_key_for_movement(movement_name)
    # TODO: Fix the default angle_key
    if angle_key is None:
        angle_key = "left_knee_left_hip_with_left_ankle_left_knee"
    anim_output_local_path = """/tmp/{}_{}_{}.mp4""".format(user_nickname,
                                                            time_stamp_start,
                                                            time_stamp_end)
    visualization_s3_key = """user_features/{}/{}_{}.json""".format(user_nickname,
                                                                    time_stamp_start,
                                                                    time_stamp_end)
    visualization_s3_bucket = s3_bucket
    video_duration = (time_stamp_end - time_stamp_start) / 1000.0
    fps = float(len(list_of_frames)) / video_duration
    _ = visualization_pipeline.run(list_of_frames,
                                   list_of_pose_features_dict,
                                   angle_key,
                                   visualization_s3_bucket,
                                   visualization_s3_key,
                                   anim_output_local_path,
                                   fps)
    user_visualization_s3_dict = {"bucket": visualization_s3_bucket, "key": visualization_s3_key}
    print("-" * 15 + "  SEND DATA TO EXPRESS  " + "-" * 15)

    features_results_dict = {"user_video_id": user_video_id,
                             "user_session": user_session_data,
                             "user_pose_features_json_file": user_features_s3_dict,
                             "user_visualization_video": user_visualization_s3_dict,
                             "user_feature_flask_job": None,
                             "user_movement_analysis_result": None}
    url = "https://api.workout.vision/user_features"
    express_response = requests.post(url, data=json.dumps(features_results_dict))

    return features_results_dict, express_response.json()


@flask_app.route("/user_features", methods=["POST", "GET"], strict_slashes=False)
def user_features():
    if request.method == "POST":
        try:
            print(request)
            request_data = request.get_json()
            print(request_data)
            with flask_app.app_context():
                task = run_features_pipeline_task.apply_async(args=[request_data])
                response = {"state": task.state,
                            "task_id": task.id,
                            "Location": url_for("task_status", task_id=task.id)}
            return jsonify(response), 202, {"Location": url_for("task_status", task_id=task.id)}
        except Exception as e:
            return "ERROR: " + str(e)

    if request.method == "GET":
        return "YO! THIS IS A MESSAGE FROM /USER_FEATURES GET"


@flask_app.route("/status/<task_id>")
def task_status(task_id):
    task = run_features_pipeline_task.AsyncResult(task_id)
    if task.state == "PENDING":
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending..."
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", "")
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == "__main__":
    flask_app.run()
