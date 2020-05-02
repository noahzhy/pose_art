from tkinter import *
import os
import glob
import time
import json
import datetime
from estimate_keypoints import SKP
from Body import Body
from collections import namedtuple


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

RES_PATH = 'arts_res'
SKP_PATH = 'skp_output'

def mk_dir(path):
    if os.path.isdir(path):
        return True
    else:
        print('[INFO] make folder')
        return True if os.mkdir(path) else False


def get_file_basename(path):
    basename = os.path.splitext(os.path.basename(path))[0]
    return basename


def load_arts_res():
    arts_res = set()
    skp_res = set()
    print('[INFO] check folder')

    if mk_dir(RES_PATH):
        arts_res = set(map(get_file_basename, glob.glob(RES_PATH + '/*')))
        print('[INFO] check arts resources: {} files'.format(len(arts_res)))

    if mk_dir(SKP_PATH):
        skp_res = set(map(get_file_basename, glob.glob(SKP_PATH + '/*')))
        print('[INFO] check skp resources: {} files'.format(len(skp_res)))

    diff = arts_res.difference(skp_res)
    if diff:
        skp = SKP()
        for i in diff:
            skp.get_skp_from_pic(os.path.join(RES_PATH, i+".jpg"))


def load_arts_skp(basename):
    with open(os.path.join(SKP_PATH, "{}.json".format(basename))) as f:
        skps = json.load(f)
        print(skps['0'])


if __name__ == "__main__":
    load_arts_res()
    load_arts_skp("003")


