import json
from collections import namedtuple
from typing import Sequence
from collections import namedtuple
from json import JSONEncoder


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

class Keypoint:
    def __init__(self, points):
        self.x = dict(points._asdict())['x']
        self.y = dict(points._asdict())['y']


class Body:
    def __init__(self, skeleton_keypoints):
        self.skeleton_keypoints = skeleton_keypoints._asdict()["joints"]
        self.parsed_keypoint = list()

    def parser(self):
        for keypoint in self.skeleton_keypoints:
            self.parsed_keypoint.append(Keypoint(keypoint))
        return self.parsed_keypoint

    def funcname(parameter_list):
        pass


if __name__ == "__main__":
    ex = [SkeletonKeypoints(joints=[Coordinate(x=163.75, y=91.25), Coordinate(x=171.25, y=168.75), Coordinate(x=108.75, y=173.75), Coordinate(x=51.25, y=218.75), Coordinate(x=11.25, y=238.75), Coordinate(x=233.75, y=166.25), Coordinate(x=288.75, y=206.25), Coordinate(x=318.75, y=238.75), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=151.25, y=81.25), Coordinate(x=176.25, y=81.25), Coordinate(x=141.25, y=96.25), Coordinate(x=198.75, y=96.25)], confidences=[0.8880429267883301, 0.7916921377182007, 0.7081862092018127, 0.3811473548412323, 0.12481366842985153, 0.7338975071907043, 0.5312833786010742, 0.19565285742282867, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9616920351982117, 0.8972093462944031, 0.5671327710151672, 0.9144231677055359], id=0)]

    for i in ex:
        body = Body(i)
        print(len(body.parser()))
