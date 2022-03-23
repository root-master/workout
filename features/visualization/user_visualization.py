"""
Creates one animation of 2D, 3D, plot.
"""
import cv2
import numpy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from features.utils.s3 import read_json_from_s3
from features.utils.s3 import get_url_video_s3
from features.utils import video
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

skeleton_2d_lines = [[0, 1], [0, 2], [1, 3], [2, 4],
                     [5, 6], [5, 7], [6, 8], [7, 9], [8, 10],
                     [11, 12], [11, 13], [12, 14], [13, 15], [14, 16]]


def extract_angle(features_list, angle_key):
    theta = [pose_dict["angle"][angle_key] for pose_dict in features_list]
    frames = list(range(len(features_list)))
    return frames, theta


def init_2d(ax1, list_of_frames, features_list):
    ax1.xaxis.set_ticklabels([])
    ax1.yaxis.set_ticklabels([])
    keypoints_2d = numpy.array(features_list[0]["pred_keypoints_2d"]).astype(int)
    frame = list_of_frames[0]
    color = (0, 255, 0)
    thickness = 8
    for line in skeleton_2d_lines:
        i = line[0]
        j = line[1]
        start_point = tuple(list(keypoints_2d[i, :2]))
        end_point = tuple(list(keypoints_2d[j, :2]))
        frame = cv2.line(frame, start_point, end_point, color, thickness)
    image = ax1.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return image


def init_plot(ax2, angle_key, features_list):
    ax2.set_xlabel("Frame Number")
    ax2.set_ylabel(angle_key)
    frames, theta_list = extract_angle(features_list, angle_key)
    line = ax2.plot(frames, theta_list, color="blue", linewidth=3.0)
    point = ax2.plot(frames[0], theta_list[0], "o", color="red", markersize=12)
    return line, point


def init_3d(ax, features_list, elev=15., azim=70):
    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])
    lines = []
    ax.view_init(elev=elev, azim=azim)
    ax.dist = 7.5
    radius = 1.4
    ax.set_xlim3d([-radius / 2, radius / 2])
    ax.set_zlim3d([0, radius])
    ax.set_ylim3d([-radius / 2, radius / 2])

    pred_keypoints_3d = features_list[0]["pred_keypoints_3d"]
    pred_keypoints_3d = numpy.array(pred_keypoints_3d)
    rot = custom_camera_params["orientation"]
    pred_keypoints_3d_world = camera_to_world(pred_keypoints_3d, R=rot, t=0)
    pred_keypoints_3d_world[:, 2] -= numpy.min(pred_keypoints_3d_world[:, 2], axis=0, keepdims=True)

    kp3d = pred_keypoints_3d_world
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
    return ax, lines, points


def animation_update_function(frame_number, frame_2d,
                              line_plot, point_plot,
                              lines_3d_ax3, points_3d_ax3,
                              lines_3d_ax4, points_3d_ax4,
                              lines_3d_ax5, points_3d_ax5,
                              angle_key, list_of_frames, features_list):
    frame_2d = update_2d(frame_number, frame_2d, list_of_frames, features_list)
    line_plot, point_plot = update_plot(frame_number, line_plot, point_plot, angle_key, features_list)
    lines_3d_ax3, points_3d_ax3 = update_3d(frame_number, lines_3d_ax3, points_3d_ax3, features_list)
    lines_3d_ax4, points_3d_ax4 = update_3d(frame_number, lines_3d_ax4, points_3d_ax4, features_list)
    lines_3d_ax5, points_3d_ax5 = update_3d(frame_number, lines_3d_ax5, points_3d_ax5, features_list)
    return frame_2d, line_plot, point_plot, lines_3d_ax3, points_3d_ax3, lines_3d_ax4, points_3d_ax4, lines_3d_ax5, points_3d_ax5


def update_2d(frame_number, image, list_of_frames, features_list):
    keypoints_2d = numpy.array(features_list[frame_number]["pred_keypoints_2d"]).astype(int)
    frame = list_of_frames[frame_number]
    color = (0, 255, 0)
    thickness = 8
    for line in skeleton_2d_lines:
        i = line[0]
        j = line[1]
        start_point = tuple(list(keypoints_2d[i, :2]))
        end_point = tuple(list(keypoints_2d[j, :2]))
        frame = cv2.line(frame, start_point, end_point, color, thickness)
    image.set_data(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return image


def update_plot(frame_number, line, point, angle_key, features_list):
    frames, theta_list = extract_angle(features_list, angle_key)
    line[0].set_xdata(frames)
    line[0].set_ydata(theta_list)
    point[0].set_xdata([frames[frame_number]])
    point[0].set_ydata([theta_list[frame_number]])
    return line, point


def update_3d(frame_number, lines, points, features_list):
    pred_keypoints_3d = features_list[frame_number]["pred_keypoints_3d"]
    pred_keypoints_3d = numpy.array(pred_keypoints_3d)
    rot = custom_camera_params["orientation"]
    pred_keypoints_3d_world = camera_to_world(pred_keypoints_3d, R=rot, t=0)
    pred_keypoints_3d_world[:, 2] -= numpy.min(pred_keypoints_3d_world[:, 2], axis=0, keepdims=True)

    kp3d = pred_keypoints_3d_world

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


def create_animation(list_of_frames, features_list, angle_key, show=False):
    fig = plt.figure()
    fig.set_size_inches(12, 8)

    gs = GridSpec(5, 12, figure=fig)
    ax1 = fig.add_subplot(gs[:2, :6])
    ax2 = fig.add_subplot(gs[:2, 7:])
    ax3 = fig.add_subplot(gs[2:, 0:4], projection="3d")
    ax4 = fig.add_subplot(gs[2:, 4:8], projection="3d")
    ax5 = fig.add_subplot(gs[2:, 8:12], projection="3d")

    frame_2d = init_2d(ax1, list_of_frames, features_list)
    line_plot, point_plot = init_plot(ax2, angle_key, features_list)
    ax3, lines_3d_ax3, points_3d_ax3 = init_3d(ax3, features_list, elev=0, azim=70)
    ax4, lines_3d_ax4, points_3d_ax4 = init_3d(ax4, features_list, elev=0, azim=70 + 50)
    ax5, lines_3d_ax5, points_3d_ax5 = init_3d(ax5, features_list, elev=0, azim=70 + 240)

    fps = 30

    anim = animation.FuncAnimation(fig, animation_update_function,
                                   fargs=(frame_2d, line_plot, point_plot,
                                          lines_3d_ax3, points_3d_ax3,
                                          lines_3d_ax4, points_3d_ax4,
                                          lines_3d_ax5, points_3d_ax5,
                                          angle_key, list_of_frames, features_list),
                                   frames=len(features_list), interval=1000 / fps, repeat=True)
    if show:
        plt.show()
    return anim
