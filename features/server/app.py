from flask import Flask, jsonify, url_for
from flask import request
from flask_cors import CORS
from celery import Celery

from features.pipeline import features_pipeline


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
def run_features_pipeline_task(request_data):
    print(request_data)
    # video_source = request_data["user_video"]["source"]
    video_source = "s3"
    s3_bucket = request_data["user_video"]["bucket"]
    s3_video_key = request_data["user_video"]["key"]
    features_source = "s3"
    user_nickname = request_data["user"]["nickname"]
    time_stamp_start = request_data["timestamp_start"]
    time_stamp_end = request_data["timestamp_end"]
    s3_features_key = """user_features/{}/{}_{}.json""".format(user_nickname,
                                                               time_stamp_start,
                                                               time_stamp_end)
    _ = features_pipeline.run(video_source=video_source,
                              s3_bucket=s3_bucket,
                              s3_video_key=s3_video_key,
                              features_source=features_source,
                              s3_features_key=s3_features_key)
    features = {"key": s3_features_key,
                "bucket": s3_bucket}
    return features


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
                            "Location": url_for("taskstatus", task_id=task.id)}
            return jsonify(response), 202, {"Location": url_for("taskstatus", task_id=task.id)}
        except Exception as e:
            return "ERROR: " + str(e)

    if request.method == "GET":
        return "YO! THIS IS A MESSAGE FROM /USER_FEATURES GET"


@flask_app.route("/status/<task_id>")
def taskstatus(task_id):
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
