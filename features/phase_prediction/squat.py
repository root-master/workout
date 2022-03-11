import numpy


def smooth(y, box_pts):
    box = numpy.ones(box_pts) / box_pts
    y_smooth = numpy.convolve(y, box, mode='same')
    return y_smooth


def get_theta_dot_dot(theta_dot):
    theta_dot_dot = numpy.diff(theta_dot)
    theta_dot_dot = numpy.append(theta_dot_dot, theta_dot[-1])
    return theta_dot_dot


def find_critical_frames(theta_dot):
    critical_frames = []
    for i in range(0, len(theta_dot) - 1):
        if theta_dot[i] * theta_dot[i + 1] < 0:
            critical_frames.append(i)
    return critical_frames


def predict_squat_phase_using_domain_knowledge(theta_dot, theta_dot_dot):
    frame_to_phases_dict = {}
    theta_dot_smooth = smooth(theta_dot, 10)
    critical_frames = find_critical_frames(theta_dot_smooth)
    for i in critical_frames:
        if theta_dot_smooth[i] < theta_dot_smooth[i + 1]:
            frame_to_phases_dict[i] = "standing"
        else:
            frame_to_phases_dict[i] = "squat"
    theta_dot_dot = get_theta_dot_dot(theta_dot)
    theta_dot_dot_smooth = smooth(theta_dot_dot, 10)
    max_min_theta_dot_frames = find_critical_frames(theta_dot_dot_smooth)
    for i in max_min_theta_dot_frames:
        if theta_dot_dot_smooth[i] < theta_dot_dot_smooth[i + 1]:
            frame_to_phases_dict[i] = "squat-to-standing"
        else:
            frame_to_phases_dict[i] = "standing-to-squat"

    phase_to_frame_dict = {}
    for k, v in frame_to_phases_dict.items():
        if v not in phase_to_frame_dict.keys():
            phase_to_frame_dict[v] = [k]
        else:
            phase_to_frame_dict[v].append(k)
    return frame_to_phases_dict, phase_to_frame_dict
