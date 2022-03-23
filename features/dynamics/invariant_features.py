"""
Extract invariant features like angles and velocities between bones.
run features/dynamics/invariant_features.py
"""
import json
from typing import Tuple, List, Dict

import numpy

from features.dynamics.features_defintions import (videoPose3D_keypoints_name_to_index_mapping_dict,
                                                   angle_features_definition_dict,
                                                   movements_angle_dict,
                                                   Z_axis)


def get_vector(initial_point: List[float], terminal_point: List[float]):
    vector = numpy.array(terminal_point) - numpy.array(initial_point)
    return vector


def calculate_angle_between_vectors(vector_1, vector_2):
    unit_vector_1 = numpy.array(vector_1) / numpy.linalg.norm(vector_1)
    unit_vector_2 = numpy.array(vector_2) / numpy.linalg.norm(vector_2)
    dot_product = numpy.dot(unit_vector_1, unit_vector_2)
    angle = numpy.arccos(dot_product)
    return angle


def get_vector_from_tuple_of_names(tuple_of_keys: Tuple[str], keypoints_3d: List[List[float]]):
    k1 = tuple_of_keys[0]
    k2 = tuple_of_keys[1]

    i1 = videoPose3D_keypoints_name_to_index_mapping_dict[k1]
    i2 = videoPose3D_keypoints_name_to_index_mapping_dict[k2]

    p1 = numpy.array(keypoints_3d[i1])
    p2 = numpy.array(keypoints_3d[i2])

    vector = p2 - p1
    return vector


def calculate_angle_between_lines(line_1, line_2, keypoints_3d: List[List[float]]) -> float:
    vec_1 = get_vector_from_tuple_of_names(line_1, keypoints_3d)

    if isinstance(line_2, str) and line_2 == "Z_axis":
        vec_2 = numpy.array(Z_axis)
    else:
        vec_2 = get_vector_from_tuple_of_names(line_2, keypoints_3d)

    angle = calculate_angle_between_vectors(vec_1, vec_2)
    return angle


def get_angle_features_from_keypoints_3d(keypoints_3d: List[List[float]]) -> Dict[str, float]:
    angle_features = {}
    for keypoint_name in angle_features_definition_dict.keys():
        line_pairs = angle_features_definition_dict[keypoint_name]
        line_1 = line_pairs[0]
        line_2 = line_pairs[1]
        angle = calculate_angle_between_lines(line_1, line_2, keypoints_3d)
        angle_features[keypoint_name] = angle
    return angle_features


def get_angle_features_from_video_keypoints_3d(keypoints_3d_list: List[List[List[float]]]) -> List[Dict]:
    angle_features_list = [get_angle_features_from_keypoints_3d(keypoints_3d) for keypoints_3d in keypoints_3d_list]
    return angle_features_list


def get_angular_velocity_from_angle_features(theta_j: Dict[str, float], theta_i: Dict[str, float], fps=30.0):
    angular_velocities_features = {}
    for name in theta_i.keys():
        angular_velocities_features[name] = (theta_j[name] - theta_i[name]) * fps
    return angular_velocities_features


def read_json(local_path: str) -> List[Dict]:
    with open(local_path) as f:
        pose_data_list = json.load(f)
    return pose_data_list


def get_angle_key_for_movement(movement_name: str):
    """
    TODO: we actually should return a list or object of angles and distances.
    TODO: Also the logic of finding key is scrappy
    """
    keys = list(movements_angle_dict.keys())
    for key in keys:
        if key in movement_name.lower():
            return movements_angle_dict[key]
    return None


def run(list_of_pose_features_dict, fps=30.0, camera_to_world_view=True):
    for frame_number, pose_features_dict in enumerate(list_of_pose_features_dict):
        pred_keypoint_3d = pose_features_dict["pred_keypoints_3d"]
        pred_keypoint_3d_world = pose_features_dict["pred_keypoints_3d_world"]
        if camera_to_world_view:
            list_of_pose_features_dict[frame_number]["angle"] = get_angle_features_from_keypoints_3d(
                pred_keypoint_3d_world)
        else:
            list_of_pose_features_dict[frame_number]["angle"] = get_angle_features_from_keypoints_3d(pred_keypoint_3d)

    for j in range(1, len(list_of_pose_features_dict)):
        i = j - 1
        theta_i = list_of_pose_features_dict[i]["angle"]
        theta_j = list_of_pose_features_dict[j]["angle"]
        list_of_pose_features_dict[i]["velocity"] = get_angular_velocity_from_angle_features(theta_j, theta_i, fps=fps)
    list_of_pose_features_dict[j]["velocity"] = list_of_pose_features_dict[i]["velocity"]
    return list_of_pose_features_dict
