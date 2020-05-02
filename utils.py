# from tkinter import *
import os
import sys
import glob
import json
import math

from Body import Body
from collections import namedtuple
from estimate_keypoints import SKP


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

RES_PATH = 'arts_res'
SKP_PATH = 'skp_output'

def load_res():
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


def get_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))


def find_closest(basename, me):
    """
    basename: basename of json file
    me: Body()
    """
    def load_arts_skp(basename):
        with open(os.path.join(SKP_PATH, "{}.json".format(basename))) as f:
            return json.loads(f.read())

    (x, y) = me.get_head_coordinates()
    res = load_arts_skp(basename)
    # print((x, y))
    # print(res)

    min_distance = sys.maxsize
    min_id = 10
    for i in res:
        dist = get_distance(x, y, res[i]['head'][0], res[i]['head'][1])
        print("dist:", dist)
        if min_distance > dist:
            min_distance = dist
            min_id = i
    return min_id


if __name__ == "__main__":
    # bodies = [SkeletonKeypoints(joints=[Coordinate(x=394.66668701171875, y=272.0), Coordinate(x=426.66668701171875, y=442.66668701171875), Coordinate(x=266.66668701171875, y=453.3333435058594), Coordinate(x=224.0, y=730.6666870117188), Coordinate(x=-1.0, y=-1.0), Coordinate(x=597.3333740234375, y=442.66668701171875), Coordinate(x=682.6666870117188, y=752.0), Coordinate(x=490.66668701171875, y=720.0), Coordinate(x=288.0, y=933.3333740234375), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=480.0, y=976.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=352.0, y=240.0), Coordinate(x=426.66668701171875, y=229.33334350585938), Coordinate(x=309.3333435058594, y=261.3333435058594), Coordinate(x=490.66668701171875, y=218.6666717529297)], confidences=[0.9431966543197632, 0.8282583951950073, 0.7755342125892639, 0.6829060912132263, 0.0, 0.8233133554458618, 0.7878410220146179, 0.840853750705719, 0.29739099740982056, 0.0, 0.0, 0.32887616753578186, 0.0, 0.0, 0.9171513319015503, 0.9690274596214294, 0.7840135097503662, 0.9125882983207703], id=0)]

    # for i in bodies:
    #     body = Body()
    #     body.set_body(i)
    #     id = find_closest("003", body)
    #     print(id)
    # i = glob.glob(os.path.join(RES_PATH, '*', '003.jpg'))
    # print(i)
    pass
