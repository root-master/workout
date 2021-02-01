"""
Workout pipeline. Show the demo to athletes and capture their performance.
"""
import os
import time

from workout.data_types.athlete import Athlete
from workout.data_types.workout_session import WorkoutSession

from workout.context import Context
from workout.video.capture import Capture
from workout.video.writer import Writer

context = Context(env="local")
input_params = context.parameters["input_params"]
athlete = Athlete(**context.parameters["athlete"][input_params["athlete"]])
workout_session = WorkoutSession()
session = context.parameters["sessions"]
pods = session[input_params["session"]]

print("=" * 60)
print("=" * 20 + " RAD WORK " + "=" * 20)
print("")

print("\a")
time.sleep(5)

for pod_i, pod in enumerate(pods):
    pod_name = pod["pod_name"]
    pod_workout = session[pod_name]

    print("=" * 20 + "POD {pod_i}: {pod_name}".format(pod_i=pod_i + 1, pod_name=pod_name) + "=" * 20)
    for workout_i, workout in enumerate(pod_workout):
        move_name = workout["move"]
        sets = workout["sets"]
        print("-" * 40)
        print("MOVE {workout_i}: {move}".format(workout_i=workout_i, move=move_name))
        print("SETS : {sets}".format(sets=sets))

        set_duration = workout["set_duration"]
        title = workout["title"]
        reps = workout["reps"]
        if reps:
            print("REPS : {reps}".format(reps=reps))
        print("SET DURATION: {duration}".format(duration=set_duration))

        if move_name == "rest":
            print(title)
            print("\a")
            time.sleep(set_duration)
            continue

        if pod["video_capture"]:
            for set_i in range(sets):
                print("\a")
                time.sleep(0.3)
                print("\a")

                cap = Capture(0, end_time=set_duration)
                print("START SET {}".format(set_i + 1))
                print("CAPTURING ... ")
                cap.capture()

                print("\a")

                video_rel_path = "data/rec/{move_name}/".format(move_name=move_name)
                directory = os.path.join(context.repo_path, video_rel_path)
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                file_name = "{workout_date}_from_{timestamp_from}_to_{timestamp_to}.avi" \
                    .format(workout_date=workout_session.workout_date,
                            timestamp_from=cap.start_timestamp,
                            timestamp_to=cap.end_timestamp)
                file_path = os.path.join(directory, file_name)
                print("WRITING TO ", file_name)

                video_writer = Writer(path=file_path,
                                      width=cap.width,
                                      height=cap.height,
                                      fps=cap.fps())
                video_writer.write_from_dict(timestamp_queues=cap.timestamp_queues,
                                             timestamp_frames_dict=cap.timestamp_frames_dict)
                time.sleep(workout["set_rest_duration"])
    print("")
print("=" * 60)
