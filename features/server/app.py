from flask import Flask
from flask import request
from flask_cors import CORS

from features.pipeline import features_pipeline

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST", "DELETE"])
def yo():
    return "YO! THIS IS A MESSAGE FROM WORKOUT VISION ML FEATURES SERVER. LOVE YOURSELF!"


@app.route("/user_features", methods=["POST", "GET"], strict_slashes=False)
def user_features():
    if request.method == "POST":
        try:
            print(request)
            request_data = request.get_json()
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
        except Exception as e:
            return "ERROR: " + str(e)

    if request.method == "GET":
        return "YO! THIS IS A MESSAGE FROM /USER_FEATURES GET"


if __name__ == "__main__":
    app.run()
