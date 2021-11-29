import numpy
import torch


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


def wrap(func, *args, unsqueeze=False):
    """
    Wrap a torch function so it can be called with NumPy arrays.
    Input and return types are seamlessly converted.
    """

    # Convert input types where applicable
    args = list(args)
    for i, arg in enumerate(args):
        if type(arg) == numpy.ndarray:
            args[i] = torch.from_numpy(arg)
            if unsqueeze:
                args[i] = args[i].unsqueeze(0)

    result = func(*args)

    # Convert output types where applicable
    if isinstance(result, tuple):
        result = list(result)
        for i, res in enumerate(result):
            if type(res) == torch.Tensor:
                if unsqueeze:
                    res = res.squeeze(0)
                result[i] = res.numpy()
        return tuple(result)
    elif type(result) == torch.Tensor:
        if unsqueeze:
            result = result.squeeze(0)
        return result.numpy()
    else:
        return result


def qrot(q, v):
    """
    Rotate vector(s) v about the rotation described by quaternion(s) q.
    Expects a tensor of shape (*, 4) for q and a tensor of shape (*, 3) for v,
    where * denotes any number of dimensions.
    Returns a tensor of shape (*, 3).
    """
    assert q.shape[-1] == 4
    assert v.shape[-1] == 3
    assert q.shape[:-1] == v.shape[:-1]

    qvec = q[..., 1:]
    uv = torch.cross(qvec, v, dim=len(q.shape) - 1)
    uuv = torch.cross(qvec, uv, dim=len(q.shape) - 1)
    return (v + 2 * (q[..., :1] * uv + uuv))


def qinverse(q, inplace=False):
    # We assume the quaternion to be normalized
    if inplace:
        q[..., 1:] *= -1
        return q
    else:
        w = q[..., :1]
        xyz = q[..., 1:]
        return torch.cat((w, -xyz), dim=len(q.shape) - 1)


def world_to_camera(X, R, t):
    Rt = wrap(qinverse, R)  # Invert rotation
    return wrap(qrot, numpy.tile(Rt, (*X.shape[:-1], 1)), X - t)  # Rotate and translate


def camera_to_world(X, R, t):
    return wrap(qrot, numpy.tile(R, (*X.shape[:-1], 1)), X) + t
