import json

from flask import Flask, jsonify, url_for
from flask import request
from flask_cors import CORS

import requests

from recommendations.workout_recommendations.data import create_fake_workout_sessions_pd
from recommendations.workout_recommendations.model import recommend_workout

flask_app = Flask(__name__)
CORS(flask_app)
df_workout_sessions = create_fake_workout_sessions_pd(num_workout_sessions=1000)


@flask_app.route("/", methods=["GET", "POST", "DELETE"])
def yo():
    return "YO! THIS IS A MESSAGE FROM WORKOUT VISION ML RECOMMENDATIONS SERVER. LOVE YOURSELF!"


@flask_app.route("/workout_session_recommendations", methods=["POST", "GET"], strict_slashes=False)
def workout_session_recommendations():
    if request.method == "POST":
        try:
            request_data = request.get_json()
            print(request_data)
            total_time_minutes = request_data["total_time_minutes"]
            avg_MET = request_data["avg_MET"]
            avg_movements_difficulty = request_data["avg_movements_difficulty"]
            input_fitness_dimensions_distribution = request_data["input_fitness_dimensions_distribution"]
            input_body_parts_distribution = request_data["input_body_parts_distribution"]
            df_recommended_session = recommend_workout(df_workout_sessions,
                                                       total_time_minutes,
                                                       avg_MET,
                                                       avg_movements_difficulty,
                                                       input_fitness_dimensions_distribution,
                                                       input_body_parts_distribution,
                                                       top_rank=0.5)
            result = df_recommended_session.to_json(orient="table")
            parsed = json.loads(result)
            print(parsed["data"][0])
            return parsed["data"][0]

        except Exception as e:
            return "ERROR: " + str(e)

    if request.method == "GET":
        return "YO! THIS IS A MESSAGE FROM /workout_sessions_recommendations GET"


if __name__ == "__main__":
    flask_app.run()
