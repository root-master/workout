"""
This module uses detectron2 to run pose_estimation on a frame

Detectron2 is Facebook AI Research's next generation library that provides
state-of-the-art detection and segmentation algorithms.

To install detectron2 see https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md
To use latest gcc for conda (that's required for detectron2) run:
conda update libgcc
"""
from typing import Dict, List

import numpy
import torch
import cv2
from tqdm import tqdm
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor
from detectron2.model_zoo import model_zoo
from detectron2.structures import Boxes
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from torch import Tensor


def get_config():
    """Prepares the config file to an specific pretrained detectron2 model. """
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    # cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml")
    cfg.MODEL.WEIGHTS = "checkpoints/model_final_997cc7.pkl"

    if torch.cuda.is_available():
        cfg.MODEL.DEVICE = "cuda"
    else:
        cfg.MODEL.DEVICE = "cpu"
    return cfg


class Detectron2_Predictor:
    def __init__(self):
        self.cfg = get_config()
        self.predictor = self.load_detectron2_model()

    def load_detectron2_model(self):
        """Creates and loads a Detectron2 model."""
        return DefaultPredictor(self.cfg)

    def infer2d(self, image: numpy.ndarray):
        """Infer the model on an input image."""
        return self.predictor(image)

    def infer2d_to_dict_of_tensors(self, image: numpy.ndarray) -> Dict:
        """Infer the model on an input image and gets the dict results."""
        output = self.infer2d(image)
        output = output["instances"].to("cpu").get_fields()
        output["image"] = {}
        output["image"]["width"] = image.shape[1]
        output["image"]["height"] = image.shape[0]
        return output

    def infer2d_to_dict_of_numpy_array(self, image: numpy.ndarray) -> Dict:
        """Infer the model on an input image and gets the dict results."""
        output = self.infer2d_to_dict_of_tensors(image)
        for k, v in output.items():
            if isinstance(v, Boxes):
                output[k] = v.tensor.numpy()
            elif isinstance(v, Tensor):
                output[k] = v.numpy()
        return output

    def run_on_video(self, list_of_frames: List[numpy.ndarray]) -> List[Dict]:
        """Runs the 2d pose estimation model on a list of frames."""
        list_of_pose_features_dict = []
        for frame_i in tqdm(range(len(list_of_frames))):
            image = list_of_frames[frame_i]
            pose_features_dict = self.infer2d_to_dict_of_numpy_array(image)
            list_of_pose_features_dict.append(pose_features_dict)
        return list_of_pose_features_dict

    def write_show_keypoints(self, image: numpy.ndarray, show: bool = True,
                             write: bool = False, result_file: str = None):
        output = self.infer2d(image)
        v = Visualizer(image[:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(output["instances"].to("cpu"))
        if write:
            result_file = result_file if result_file else "test_data/test_images/test_output.jpg"
            cv2.imwrite(result_file, out.get_image()[:, :, ::-1])
        if show:
            cv2.imshow("show", out.get_image()[:, :, ::-1])
