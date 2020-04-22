import pyrealsense2 as rs
import numpy as np
import platform
import argparse
import cv2
import os

from pprint import pprint
from cubemos.core.nativewrapper import CM_TargetComputeDevice
from cubemos.core.nativewrapper import initialise_logging, CM_LogLevel
from cubemos.skeleton_tracking.nativewrapper import Api, SkeletonKeypoints


confidence_threshold = 0.35
skeleton_color = np.random.randint(256, size=3).tolist()

pipe = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 320, 240, rs.format.bgr8, 30)
pipe.start(config)

keypoint_ids = [
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
    (5, 6),
    (6, 7),
    (1, 8),
    (8, 9),
    (9, 10),
    (1, 11),
    (11, 12),
    (12, 13),
    (1, 0),
    (0, 14),
    (14, 16),
    (0, 15),
    (15, 17),
]


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
            "Please have a look at the Getting Started Guide on how to "
            "use the post-installation script to generate the license file")
    if "CUBEMOS_SKEL_SDK" not in os.environ:
        raise Exception(
            "The environment Variable \"CUBEMOS_SKEL_SDK\" is not set. "
            "Please check the troubleshooting section in the Getting "
            "Started Guide to resolve this issue." 
        )


def get_valid_limbs(keypoint_ids, skeleton, confidence_threshold):
    limbs = [
        (tuple(map(int, skeleton.joints[i])), tuple(map(int, skeleton.joints[v])))
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


if __name__ == "__main__":
    try:
        check_license_and_variables_exist()
        sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
        # initialize the api with a valid license key in default_license_dir()
        api = Api(default_license_dir())
        model_path = os.path.join(
            sdk_path,
            "models",
            "skeleton-tracking",
            "fp32",
            "skeleton-tracking.cubemos"
        )
        api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

        while True:
            frames = pipe.wait_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())

            skeletons = api.estimate_keypoints(color_image, 192)
            print(skeletons)
            # perform inference again to demonstrate tracking functionality.
            # usually you would estimate the keypoints on another image and then
            # update the tracking id
            new_skeletons = api.estimate_keypoints(color_image, 192)
            new_skeletons = api.update_tracking_id(skeletons, new_skeletons)
            # render the points
            render_result(skeletons, color_image, confidence_threshold)

            cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
            cv2.imshow("preview", color_image)
            
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

    except Exception as ex:
        print("Exception occured: \"{}\"".format(ex))

    finally:
        pipe.stop()
