import pyrealsense2 as rs
import numpy as np
import platform
import argparse
import random
import cv2
import os

from pprint import pprint
from cubemos.core.nativewrapper import CM_TargetComputeDevice
from cubemos.core.nativewrapper import initialise_logging, CM_LogLevel
from cubemos.skeleton_tracking.nativewrapper import Api, SkeletonKeypoints

from Body import Body
from utils import *


# correct answer maintain time (seconds)
correct_maintain_time = 3
correct_rate = 90
confidence_threshold = 0.5
skeleton_color = np.random.randint(256, size=3).tolist()

width, height = (1280, 720)
pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
pipe.start(config)

keypoint_ids = [
    (1, 2), (1, 5), (2, 3), (3, 4), (5, 6), (6, 7), (1, 8),
    (8, 9), (9, 10), (1, 11), (11, 12), (12, 13), (1, 0),
]

SUCCESS_POSED = False
TIMER_STARTING = False
NUM_POSERONS = 1


def default_log_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "logs")
    elif platform.system() == "Linux":
        return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "logs")
    else:
        raise Exception("{} is not supported".format(platform.system()))


def default_license_dir():
    if platform.system() == "Windows":
        return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "license")
    elif platform.system() == "Linux":
        return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license")
    else:
        raise Exception("{} is not supported".format(platform.system()))


def check_license_and_variables_exist():
    license_path = os.path.join(default_license_dir(), "cubemos_license.json")
    if not os.path.isfile(license_path):
        raise Exception(
            "The license file has not been found at location \"" +
            default_license_dir() + "\". "
        )
    if "CUBEMOS_SKEL_SDK" not in os.environ:
        raise Exception(
            "The environment Variable \"CUBEMOS_SKEL_SDK\" is not set. "
        )


def get_valid_limbs(keypoint_ids, skeleton, confidence_threshold):
    limbs = [
        (tuple(map(int, skeleton.joints[i])),
         tuple(map(int, skeleton.joints[v])))
        for (i, v) in keypoint_ids
        if skeleton.confidences[i] >= confidence_threshold
        and skeleton.confidences[v] >= confidence_threshold
    ]
    valid_limbs = [
        limb
        for limb in limbs
        if limb[0][0] >= 0 and limb[0][1] >= 0 and limb[1][0] >= 0 and limb[1][1] >= 0
    ]
    return valid_limbs


def render_result(skeletons, img, confidence_threshold):
    for index, skeleton in enumerate(skeletons):
        limbs = get_valid_limbs(keypoint_ids, skeleton, confidence_threshold)
        for limb in limbs:
            cv2.line(
                img,
                limb[0],
                limb[1],
                skeleton_color,
                thickness=2,
                lineType=cv2.LINE_AA
            )


def run(render=False, depth=1500, conts_line_color=(256,256,256)):
    try:
        check_license_and_variables_exist()
        sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
        api = Api(default_license_dir())
        model_path = os.path.join(
            sdk_path,
            "models",
            "skeleton-tracking",
            "fp32",
            "skeleton-tracking.cubemos"
        )
        api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

        
        res = random.choice(load_res_by_persons(NUM_POSERONS))
        base = init_windows(res)

        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            color_image = cv2.flip(color_image, 1)

            skeletons = api.estimate_keypoints(color_image, 192)
            new_skeletons = api.estimate_keypoints(color_image, 192)
            new_skeletons = api.update_tracking_id(skeletons, new_skeletons)

            if render: render_result(skeletons, color_image, confidence_threshold)

            correct_score = int(compare_multi_users(skeletons, get_file_basename(res))*100)
            conts_draw = base.copy()

            if correct_score > correct_rate:
                cv2.putText(conts_draw, "{}".format(
                    correct_score), (width-100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(conts_draw, "{}".format(
                    correct_score), (width-100, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

            frames = pipe.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            if not depth_frame: continue
            depth_image = np.fliplr(np.asanyarray(depth_frame.get_data()))
            depth_image = np.uint8(np.where((depth_image >= 100) & (depth_image <= depth), 255, 0))
            depth_image = cv2.bilateralFilter(depth_image, 9, 100, 100)
            contours, hierarchy = cv2.findContours(depth_image, cv2.RETR_TREE, 1)
            cv2.drawContours(conts_draw, contours, -1, conts_line_color, 5)

            cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("preview", conts_draw)

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    except Exception as e:
        print("Exception occured: \"{}\"".format(e))

    finally:
        pipe.stop()


if __name__ == "__main__":
    run()
    # base = init_windows('arts_res/001_001.jpg', True)
    # show_contours(base)
