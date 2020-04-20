from cubemos.core.nativewrapper import CM_TargetComputeDevice
from cubemos.core.nativewrapper import initialise_logging, CM_LogLevel
from cubemos.skeleton_tracking.nativewrapper import Api, SkeletonKeypoints
import cv2
import argparse
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
    skeleton_color = (100, 254, 213)
    for index, skeleton in enumerate(skeletons):
        limbs = get_valid_limbs(keypoint_ids, skeleton, confidence_threshold)
        for limb in limbs:
            cv2.line(
                img, limb[0], limb[1], skeleton_color, thickness=2, lineType=cv2.LINE_AA
            )


parser = argparse.ArgumentParser(description="Perform keypoing estimation on an image")
parser.add_argument(
    "-c",
    "--confidence_threshold",
    type=float,
    default=0.5,
    help="Minimum confidence (0-1) of displayed joints",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Increase output verbosity by enabling backend logging",
)

parser.add_argument(
    "-o",
    "--output_image",
    type=str,
    default="output/002.jpg",
    help="filename of the output image",
)

parser.add_argument(
    "--image",
    metavar="I",
    default="arts_res/002.jpg",
    type=str,
    help="filename of the input image"
)



# Main content begins
if __name__ == "__main__":
    try:
        #Parse command line arguments
        args = parser.parse_args()
        check_license_and_variables_exist()
        #Get the path of the native libraries and ressource files
        sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
        if args.verbose:
            initialise_logging(sdk_path, CM_LogLevel.CM_LL_DEBUG, True, default_log_dir())

        img = cv2.imread(args.image)
        #initialize the api with a valid license key in default_license_dir()
        api = Api(default_license_dir())
        model_path = os.path.join(
            sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos"
        )
        api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)
        #perform inference
        skeletons = api.estimate_keypoints(img, 192)

        # perform inference again to demonstrate tracking functionality.
        # usually you would estimate the keypoints on another image and then
        # update the tracking id
        new_skeletons = api.estimate_keypoints(img, 192)
        new_skeletons = api.update_tracking_id(skeletons, new_skeletons)

        render_result(skeletons, img, args.confidence_threshold)
        print("Detected skeletons: ", len(skeletons))
        if args.verbose:
          print(skeletons)
          
        if args.output_image:
            isSaved = cv2.imwrite(args.output_image, img)
            if isSaved:
                print("The result image is saved in: ", args.output_image)
            else:
                print("Saving the result image failed for the given path: ", args.output_image)


            
    except Exception as ex:
        print("Exception occured: \"{}\"".format(ex))
# Main content ends
