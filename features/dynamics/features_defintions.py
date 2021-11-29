coco_keypoints = [
                     "nose", "left_eye", "right_eye", "left_ear", "right_ear",
                     "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
                     "left_wrist", "right_wrist", "left_hip", "right_hip",
                     "left_knee", "right_knee", "left_ankle", "right_ankle"
                 ],
coco_skeleton = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7],
    [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]
]

coco_keypoints_index_to_name_mapping_dict = {
    0: "nose",
    1: "left_eye",
    2: "right_eye",
    3: "left_ear",
    4: "right_ear",
    5: "left_shoulder",
    6: "right_shoulder",
    7: "left_elbow",
    8: "right_elbow",
    9: "left_wrist",
    10: "right_wrist",
    11: "left_hip",
    12: "right_hip",
    13: "left_knee",
    14: "right_knee",
    15: "left_ankle",
    16: "right_ankle"
}

videoPose3D_skeleton = [
    [6, 5], [5, 4], [3, 2], [2, 1], [0, 1], [0, 4], [0, 7], [7, 8], [8, 9], [9, 10],
    [11, 4], [11, 12], [12, 13], [14, 1], [14, 15], [15, 16], [11, 14], [11, 7], [14, 7]
]

videoPose3D_keypoints_index_to_name_mapping_dict = {
    0: "center_hip",
    1: "left_hip",
    2: "left_knee",
    3: "left_ankle",
    4: "right_hip",
    5: "right_knee",
    6: "right_ankle",
    7: "mid_section",
    8: "neck",
    9: "nose",
    10: "head",
    11: "right_shoulder",
    12: "right_elbow",
    13: "right_wrist",
    14: "left_shoulder",
    15: "left_elbow",
    16: "left_wrist"
}

videoPose3D_keypoints_name_to_index_mapping_dict = {}
for k, v in videoPose3D_keypoints_index_to_name_mapping_dict.items():
    videoPose3D_keypoints_name_to_index_mapping_dict[v] = k

angle_features_definition_list = [
    [("left_knee", "left_hip"), ("left_ankle", "left_knee")],
    [("right_knee", "right_hip"), ("right_ankle", "right_knee")],
    # [("left_hip", "left_shoulder"), ("left_knee", "left_hip")],
    # [("right_hip", "right_shoulder"), ("right_knee", "right_hip")],
    #
    # [("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist")],
    # [("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist")],
    # [("left_shoulder", "left_elbow"), ("left_shoulder", "left_hip")],
    # [("right_shoulder", "right_elbow"), ("right_shoulder", "right_hip")],
    # [("left_shoulder", "left_elbow"), ("left_shoulder", "left_hip")],
    # [("right_shoulder", "right_elbow"), ("right_shoulder", "right_hip")],
    # [("left_shoulder", "left_wrist"), ("left_shoulder", "right_shoulder")],
    # [("right_shoulder", "right_wrist"), ("right_shoulder", "left_shoulder")],
    #
    # [("neck", "head"), ("right_shoulder", "left_shoulder")],
    # [("neck", "head"), ("center_hip", "mid_section")],
    # [("neck", "nose"), ("right_shoulder", "left_shoulder")],
    # [("center_hip", "mid_section"), ("right_hip", "left_hip")],
    #
    # [("right_hip", "right_knee"), ("left_hip", "left_knee")],
    # [("right_shoulder", "left_shoulder"), ("right_hip", "left_hip")],
    # [("right_shoulder", "left_shoulder"), ("right_knee", "left_knee")],
    # [("right_shoulder", "left_shoulder"), ("right_ankle", "left_ankle")],
    # [("right_hip", "left_hip"), ("right_knee", "left_knee")],
    # [("right_hip", "left_hip"), ("right_ankle", "left_ankle")],
    # [("right_wrist", "left_wrist"), ("right_hip", "left_hip")],
    #
    # [("left_ankle", "left_knee"), "Z_axis"],
    # [("right_ankle", "right_knee"), "Z_axis"],
    # [("left_knee", "left_hip"), "Z_axis"],
    # [("right_knee", "right_hip"), "Z_axis"],
    # [("left_hip", "left_shoulder"), "Z_axis"],
    # [("right_hip", "right_shoulder"), "Z_axis"],
    # [("left_knee", "left_shoulder"), "Z_axis"],
    # [("right_knee", "right_shoulder"), "Z_axis"],
    # [("left_ankle", "left_shoulder"), "Z_axis"],
    # [("right_ankle", "right_shoulder"), "Z_axis"],
    # [("center_hip", "mid_section"), "Z_axis"],
    # [("neck", "head"), "Z_axis"],
    # [("neck", "nose"), "Z_axis"],
]

angle_features_name_list = []
for vector_list in angle_features_definition_list:
    vector_1 = vector_list[0]
    vector_2 = vector_list[1]
    k = ""
    k += vector_1[0] + "_" + vector_1[1]
    if isinstance(vector_2, str):
        k += "_with_" + vector_2
    else:
        k += "_with_" + vector_2[0] + "_" + vector_2[1]
    angle_features_name_list.append(k)

angle_features_definition_dict = {}
for index, vector_list in enumerate(angle_features_definition_list):
    k = angle_features_name_list[index]
    angle_features_definition_dict[k] = vector_list

X_axis = [1, 0, 0]
Y_axis = [0, 1, 0]
Z_axis = [0, -1, 0]

relative_distance_features_list = [
    [("left_ankle", "right_ankle"), ("left_shoulder", "right_shoulder")]
]
