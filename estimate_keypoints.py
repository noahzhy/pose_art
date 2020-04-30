from cubemos.core.nativewrapper import CM_TargetComputeDevice
from cubemos.core.nativewrapper import initialise_logging, CM_LogLevel
from cubemos.skeleton_tracking.nativewrapper import Api, SkeletonKeypoints
import cv2
import os
import platform
from pprint import pprint

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
            "use the post-installation script to generate the license file")
    if "CUBEMOS_SKEL_SDK" not in os.environ:
        raise Exception(
            "The environment Variable \"CUBEMOS_SKEL_SDK\" is not set. "
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
    skeleton_color = (100, 254, 213)
    for index, skeleton in enumerate(skeletons):
        limbs = get_valid_limbs(keypoint_ids, skeleton, confidence_threshold)
        for limb in limbs:
            cv2.line(img, limb[0], limb[1], skeleton_color, thickness=2, lineType=cv2.LINE_AA)


class SKP:
    def __init__(self):
        super().__init__()
        check_license_and_variables_exist()
        self.confidence_threshold = 0.5
        self.output_path = "output"
        self.skp_output_path = "skp_output"
        self.api = Api(default_license_dir())
        self.model_path = os.path.join(
            os.environ["CUBEMOS_SKEL_SDK"], "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos"
        )
        self.api.load_model(CM_TargetComputeDevice.CM_CPU, self.model_path)

    def get_skp_from_pic(self, pic_path):
        try:
            print(pic_path)
            img = cv2.imread(pic_path)
            skeletons = self.api.estimate_keypoints(img, 192)
            render_result(skeletons, img, self.confidence_threshold)
            file_name = os.path.basename(pic_path)
            with open("{}/{}.txt".format(self.skp_output_path, os.path.splitext(file_name)[0]), "w") as f:
                f.write(str(skeletons))

            isSaved = cv2.imwrite("{}/{}".format(self.output_path, file_name), img)
            if isSaved:
                return True
            else:
                print("has")

        except Exception as ex:
            print("Exception occured: \"{}\"".format(ex))


if __name__ == "__main__":
    skp = SKP()
    skp.get_skp_from_pic("arts_res/001.jpg")
