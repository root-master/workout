"""
This module uses Facebook's Extract 3d from 2d
See https://github.com/facebookresearch/VideoPose3D
"""
from typing import List, Dict

import numpy
import torch

from ml.features.pose_estimation.inference_3d.generators import UnchunkedGenerator
from ml.features.pose_estimation.inference_3d.model import TemporalModel
from ml.features.pose_estimation.inference_3d.utils import normalize_screen_coordinates, index_of_largest_bbox


class VideoPose3d_coco_predictor:
    def __init__(self):
        self.kps_left = [1, 3, 5, 7, 9, 11, 13, 15]
        self.kps_right = [2, 4, 6, 8, 10, 12, 14, 16]
        self.keypoints_symmetry = [self.kps_left] + [self.kps_right]
        self.joints_right = [1, 2, 3, 14, 15, 16]
        self.joints_left = [4, 5, 6, 11, 12, 13]
        self.joints = 17
        self.load_model()
        self.load_weights()

    def load_model(self):
        """Loads VideoPose3d model."""
        self.model = TemporalModel(num_joints_in=self.joints, in_features=2, num_joints_out=self.joints,
                                   filter_widths=[3, 3, 3, 3, 3], causal=False, dropout=0.25,
                                   channels=1024,
                                   dense=False)
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def load_weights(self, path_to_model_weights="checkpoints/pretrained_h36m_detectron_coco.bin"):
        """Loads weights from a local path."""
        map_location = None if torch.cuda.is_available() else torch.device("cpu")
        checkpoint = torch.load(path_to_model_weights, map_location=map_location)
        self.model.load_state_dict(checkpoint["model_pos"])
        with torch.no_grad():
            self.model.eval()

    def extract_keypoints_from_detectron2_output(self, inference_2d_list: List[Dict]) -> numpy.array:
        """
        Extract bbox and keypoints for the biggest bbox
        from the list of dict where that dict is output of Detectron2_Prediction.

        TODO: make it work for all the instances.
        """
        keypoints_2d = numpy.zeros((len(inference_2d_list), self.joints, 2))
        keypoints_2d_normalized = numpy.zeros((len(inference_2d_list), self.joints, 2))
        for t, pose_features_dict in enumerate(inference_2d_list):
            i = index_of_largest_bbox(pose_features_dict["pred_boxes"])
            kps_2d = pose_features_dict["pred_keypoints"][i]
            keypoints_2d[t, :, :] = kps_2d[:, :2]
            width = pose_features_dict["image"]["width"]
            height = pose_features_dict["image"]["height"]
            keypoints_2d_normalized = normalize_screen_coordinates(keypoints_2d, width, height)
        return keypoints_2d, keypoints_2d_normalized

    def infer3d(self, keypoints_2d):
        receptive_field = self.model.receptive_field()
        pad = (receptive_field - 1) // 2  # Padding on each side

        test_generator = UnchunkedGenerator(None, None, [keypoints_2d],
                                            pad=pad, causal_shift=0, augment=True,
                                            kps_left=self.kps_left, kps_right=self.kps_right,
                                            joints_left=self.joints_left,
                                            joints_right=self.joints_right)
        with torch.no_grad():
            self.model.eval()
            for _, _, batch_2d in test_generator.next_epoch():
                inputs_2d = torch.from_numpy(batch_2d.astype("float32"))
                if torch.cuda.is_available():
                    inputs_2d = inputs_2d.cuda()

                predicted_3d_pos = self.model(inputs_2d)

                # Test-time augmentation (if enabled)
                if test_generator.augment_enabled():
                    # Undo flipping and take average with non-flipped version
                    predicted_3d_pos[1, :, :, 0] *= -1
                    predicted_3d_pos[1, :, self.joints_left + self.joints_right] = \
                        predicted_3d_pos[1, :, self.joints_right + self.joints_left]
                    predicted_3d_pos = torch.mean(predicted_3d_pos, dim=0, keepdim=True)
        keypoints_3d = predicted_3d_pos.squeeze(0).cpu().numpy()
        return keypoints_3d
