coco_keypoints_mapping_dict = {
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

videoPose3D_keypoints_index_to_joints_mapping_dict = {
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
    13: "right_hand",
    14: "left_shoulder",
    15: "left_elbow",
    16: "left_hand"
}

videoPose3D_keypoints_joints_to_index_mapping_dict = {}
for k, v in videoPose3D_keypoints_index_to_joints_mapping_dict.items():
    videoPose3D_keypoints_joints_to_index_mapping_dict[v] = k

custom_camera_params = {
    "orientation": [0.1407056450843811, -0.1500701755285263, -0.755240797996521, 0.6223280429840088],
    "translation": [1841.1070556640625, 4955.28466796875, 1563.4454345703125],
}
