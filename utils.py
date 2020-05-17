# from tkinter import *
import os
import cv2
import sys
import glob
import json
import operator
import numpy as np
# import pyrealsense2 as rs

from scipy import stats
from collections import namedtuple
from estimate_keypoints import SKP
from Body import Body


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

RES_PATH = 'arts_res'
SKP_PATH = 'skp_output'

def check_res():
    def mk_dir(path):
        if not os.path.isdir(path):
            print('[INFO] make folder')
            return True if os.mkdir(path) else False
        return True

    def get_file_basename(path):
        return os.path.splitext(os.path.basename(path))[0]

    arts_res = set()
    skp_res = set()
    print('[INFO] check folder')

    if mk_dir(RES_PATH):
        arts_res = set(map(get_file_basename, glob.glob(os.path.join(RES_PATH, '*.jpg'))))
        print('[INFO] check arts resources: {} files'.format(len(arts_res)))

    if mk_dir(SKP_PATH):
        skp_res = set(map(get_file_basename, glob.glob(os.path.join(SKP_PATH, '*.json'))))
        print('[INFO] check skp resources: {} files'.format(len(skp_res)))

    diff = arts_res.difference(skp_res)
    if diff:
        skp = SKP()
        for i in diff:
            skp.get_skp_from_pic(os.path.join(RES_PATH, '{}.jpg'.format(i)))


def load_arts_skp(basename):
    """
    load_arts_skp: basename of json data file
    """
    with open(os.path.join(SKP_PATH, "{}.json".format(basename))) as f:
        return json.loads(f.read())


def load_res_by_persons(num):
    res_support = glob.glob(os.path.join(RES_PATH, '{:03d}_*.jpg'.format(num)))
    if not res_support:
        # to return list to keep same format
        return [os.path.join(RES_PATH, '999_000.jpg')]
    return res_support


def init_windows(img, test_mode=False):
    base = cv2.imread('bg.jpg')
    
    if test_mode:
        base = cv2.resize(base, (1280, 720))

    img = cv2.imread(img)
    h, w, _ = img.shape
    scale_percent = 60       # percent of original size
    height = int(h * scale_percent / 100)
    width = int(w * scale_percent / 100)
    dim = (width, height)

    img_resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    base[0:height, 0:width] = img_resized
    
    # cv2.namedWindow("preview", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("preview", bg)
    # cv2.waitKey()

    return base




# def compare_multi_users(multi_users_skps, standard_file_path):
#     total_score = 0.0
#     standard_ans_stack = load_arts_skp(standard_file_path)
#     num_standard = len(standard_ans_stack)
#     min_detected_keypoints = 4
#     users_stack = [Body(i) for i in multi_users_skps]

#     for i in users_stack:
#         candidates = dict()
#         for num in standard_ans_stack:
#             users, standard = list(), list()
#             for (x, y) in zip(i.calculate_angles(), standard_ans_stack[num]['angles']):
#                 if x >= 0 and y >= 0:
#                     users.append(x)
#                     standard.append(y)

#             if len(users) >= min_detected_keypoints:
#                 p = stats.pearsonr(users, standard)
#                 p = p[0] if not (p[-1] > 0.5 and p[0]) < 0 else -p[0]
#                 candidates[str(num)] = p

#         if candidates:
#             match_idx = max(candidates.items(), key=operator.itemgetter(1))[0]
#             del standard_ans_stack[match_idx]
#             total_score += candidates[match_idx]

#     return round(total_score/num_standard, 2)


def compare_multi_users(multi_users_skps, standard_file_path):
    total_score = 0.0
    # error_rate = 15
    standard_ans_stack = load_arts_skp(standard_file_path)
    num_standard = len(standard_ans_stack)
    min_detected_keypoints = 4
    users_stack = [Body(i) for i in multi_users_skps]

    for i in users_stack:
        candidates = dict()
        for num in standard_ans_stack:
            score = i.compare_skps_angles(standard_ans_stack[num]['angles'])
            candidates[str(num)] = score

        if candidates:
            match_idx = max(candidates.items(), key=operator.itemgetter(1))[0]
            del standard_ans_stack[match_idx]
            total_score += candidates[match_idx]

    return round(total_score/num_standard, 2)


if __name__ == "__main__":
    bodies = [
        SkeletonKeypoints(
            joints=[
                Coordinate(x=241.25, y=78.75), Coordinate(x=233.75, y=121.25), Coordinate(x=201.25, y=116.25), 
                Coordinate(x=188.75, y=168.75), Coordinate(x=196.25, y=203.75), Coordinate(x=263.75, y=126.25),
                Coordinate(x=258.75, y=181.25), Coordinate(x=251.25, y=211.25), Coordinate(x=198.75, y=211.25), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=236.25, y=218.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=236.25, y=68.75), 
                Coordinate(x=248.75, y=73.75), Coordinate(x=226.25, y=73.75), Coordinate(x=261.25, y=81.25)
            ],
            confidences=[
                0.9365450143814087, 0.8258265256881714, 0.7434385418891907, 
                0.5684559941291809, 0.20085489749908447, 0.7587136030197144, 
                0.2790355086326599, 0.1256263554096222, 0.28881335258483887, 
                0.0, 0.0, 0.29619401693344116,
                0.0, 0.0, 0.9608742594718933,
                0.9468154311180115, 0.8347669243812561, 0.8204925060272217
            ], 
            id=0
        ), 
        
        SkeletonKeypoints(
            joints=[
                Coordinate(x=133.75, y=53.75), Coordinate(x=138.75, y=113.75), Coordinate(x=96.25, y=131.25), 
                Coordinate(x=98.75, y=153.75), Coordinate(x=-1.0, y=-1.0), Coordinate(x=176.25, y=91.25), 
                Coordinate(x=178.75, y=121.25), Coordinate(x=156.25, y=93.75), Coordinate(x=133.75, y=228.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=176.25, y=228.75), 
                Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=116.25, y=53.75), 
                Coordinate(x=138.75, y=41.25), Coordinate(x=103.75, y=78.75), Coordinate(x=153.75, y=48.75)
            ], 
            confidences=[
                0.8488292694091797, 0.6395670175552368, 0.6180622577667236, 
                0.21119025349617004, 0.0, 0.48279309272766113, 
                0.21377024054527283, 0.5299386978149414, 0.21255280077457428, 
                0.0, 0.0, 0.22222042083740234, 
                0.0, 0.0, 0.8606398105621338, 
                0.9005011320114136, 0.8303616046905518, 0.20512905716896057
            ], 
            id=1
        )
    ]

    # count = 0
    # while count < 1:
    #     count += 1
    #     score = compare_multi_users(bodies, '999_000')
    #     print(score)


    res_for_show = load_res_by_persons(len(bodies))
    print(res_for_show)

    base = init_windows('arts_res/001_001.jpg', True)
    show_contours(base)
