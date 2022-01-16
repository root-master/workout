import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from features.pose_estimation.inference_3d.utils import camera_to_world

custom_camera_params = {
    "azimuth": 70,  # Only used for visualization
    "orientation": [0.1407056450843811, -0.1500701755285263, -0.755240797996521, 0.6223280429840088],
    "translation": [1841.1070556640625, 4955.28466796875, 1563.4454345703125],
}

videoPose3D_skeleton = [
    [6, 5], [5, 4], [3, 2], [2, 1], [0, 1], [0, 4], [0, 7], [7, 8], [8, 9], [9, 10],
    [11, 4], [11, 12], [12, 13], [14, 1], [14, 15], [15, 16], [11, 14]
]


def visualize_one_frame_3d(frame_number, features_list, world_view=True):
    pred_keypoint_3d = features_list[frame_number]["pred_keypoint_3d"]
    pred_keypoint_3d = numpy.array(pred_keypoint_3d)
    rot = custom_camera_params["orientation"]
    pred_keypoint_3d_world = camera_to_world(pred_keypoint_3d, R=rot, t=0)
    pred_keypoint_3d_world[:, 2] -= numpy.min(pred_keypoint_3d_world[:, 2], axis=0, keepdims=True)
    if world_view:
        kp3d = pred_keypoint_3d_world
    else:
        kp3d = pred_keypoint_3d
    xs = kp3d[:, 0]
    ys = kp3d[:, 1]
    zs = kp3d[:, 2]

    ax = plt.axes(projection="3d")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=15., azim=custom_camera_params["azimuth"])
    ax.dist = 7.5
    # ax.set_box_aspect([1, 1, 1.1])
    radius = 1.4
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_zlim3d([0, radius])
    ax.set_ylim3d([-radius / 2, radius / 2])

    ax.plot3D(xs, ys, zs, "o", color="red", linewidth=4.0)

    for points_pair in videoPose3D_skeleton:
        i1 = points_pair[0]
        i2 = points_pair[1]
        p1 = [kp3d[i1, 0], kp3d[i1, 1], kp3d[i1, 2]]
        p2 = [kp3d[i2, 0], kp3d[i2, 1], kp3d[i2, 2]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="blue", linewidth=3.0)
    plt.show()


def update_3d_pose(frame_number, lines, points, features_list):
    pred_keypoint_3d = features_list[frame_number]["pred_keypoint_3d"]
    pred_keypoint_3d = numpy.array(pred_keypoint_3d)
    rot = custom_camera_params["orientation"]
    pred_keypoint_3d_world = camera_to_world(pred_keypoint_3d, R=rot, t=0)
    pred_keypoint_3d_world[:, 2] -= numpy.min(pred_keypoint_3d_world[:, 2], axis=0, keepdims=True)

    kp3d = pred_keypoint_3d_world

    xs = kp3d[:, 0]
    ys = kp3d[:, 1]
    zs = kp3d[:, 2]

    points[0].set_xdata(numpy.array(xs))
    points[0].set_ydata(numpy.array(ys))
    points[0].set_3d_properties(numpy.array(zs), zdir="z")

    for j, points_pair in enumerate(videoPose3D_skeleton):
        i1 = points_pair[0]
        i2 = points_pair[1]
        p1 = [kp3d[i1, 0], kp3d[i1, 1], kp3d[i1, 2]]
        p2 = [kp3d[i2, 0], kp3d[i2, 1], kp3d[i2, 2]]

        lines[j][0].set_xdata(numpy.array([p1[0], p2[0]]))
        lines[j][0].set_ydata(numpy.array([p1[1], p2[1]]))
        lines[j][0].set_3d_properties(numpy.array([p1[2], p2[2]]), zdir="z")
    return lines, points


def animate(features_list, fps=30):
    fig = plt.figure()
    ax = plt.axes(projection="3d")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=15., azim=custom_camera_params["azimuth"])
    ax.dist = 7.5
    #     ax.set_box_aspect([1,1,1.1])
    radius = 1.4
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_zlim3d([0, radius])
    ax.set_ylim3d([-radius / 2, radius / 2])

    lines = []

    pred_keypoint_3d = features_list[0]["pred_keypoint_3d"]
    pred_keypoint_3d = numpy.array(pred_keypoint_3d)
    rot = custom_camera_params["orientation"]
    pred_keypoint_3d_world = camera_to_world(pred_keypoint_3d, R=rot, t=0)
    pred_keypoint_3d_world[:, 2] -= numpy.min(pred_keypoint_3d_world[:, 2], axis=0, keepdims=True)

    kp3d = pred_keypoint_3d_world
    xs = kp3d[:, 0]
    ys = kp3d[:, 1]
    zs = kp3d[:, 2]
    points = ax.plot3D(xs, ys, zs, "o", color="red", linewidth=4.0)

    for points_pair in videoPose3D_skeleton:
        i1 = points_pair[0]
        i2 = points_pair[1]
        p1 = [kp3d[i1, 0], kp3d[i1, 1], kp3d[i1, 2]]
        p2 = [kp3d[i2, 0], kp3d[i2, 1], kp3d[i2, 2]]
        lines.append(ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="blue", linewidth=3.0, zdir="z"))

    anim = animation.FuncAnimation(fig, update_3d_pose, fargs=(lines, points, features_list),
                                   frames=len(features_list), interval=1000 / fps, repeat=True)
    return anim
