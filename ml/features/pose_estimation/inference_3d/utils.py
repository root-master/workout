import numpy


def normalize_screen_coordinates(keypoints: numpy.array, width, height) -> numpy.ndarray:
    """Normalizes the coordinates.

    x_hat = 2 * x/w - 1
    y_hat = 2 * y/w - h/w
    """
    assert keypoints.shape[-1] == 2

    # Normalize so that [0, w] is mapped to [-1, 1], while preserving the aspect ratio
    return keypoints / width * 2 - numpy.array([1, height / width])


def image_coordinates(keypoints: numpy.array, width, height) -> numpy.ndarray:
    """Denormalizes the coordinates back to image coordinates."""

    return (keypoints + [1, height / width]) * width / 2


def calculate_bbox_area(bbox_array: numpy.ndarray):
    """Calculates bbox area given a bbox array for one."""
    area = (bbox_array[:, 2] - bbox_array[:, 0]) * (bbox_array[:, 3] - bbox_array[:, 1])
    return area


def index_of_largest_bbox_area(bbox_area_array: numpy.ndarray):
    """Returns index of the largest bbox given the area array."""
    return numpy.argmax(bbox_area_array)


def index_of_largest_bbox(bbox_array: numpy.ndarray):
    """Returns index of the largest bbox given the bbox array."""
    return index_of_largest_bbox_area(calculate_bbox_area(bbox_array))

# bbox_array = numpy.array([[1001.1964, 44.16782, 1319.5095, 715.56433],
#                           [730.33655, 19.212332, 947.7073, 740.1717],
#                           [18.052113, 52.585373, 247.1843, 726.01605],
#                           [369.73257, 39.6811, 606.3058, 718.88055]])
#
# bbox_area = calculate_bbox_area(bbox_array)
# i = index_of_largest_bbox_area(bbox_area)
# run ml/features/pose_estimation/inference_3d/utils.py
