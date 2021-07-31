"""
Visualization tools.
run ml/features/pose_estimation/visualization/visualize.py
"""
import json


def load_json(path_to_json: str):
    with open(path_to_json) as f:
        data = json.load(f)
    return data
