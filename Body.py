import json
from collections import namedtuple
from typing import Sequence
from collections import namedtuple
from json import JSONEncoder
import numpy as np


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

class Keypoint:
    def __init__(self, points):
        self.x = dict(points._asdict())['x']
        self.y = dict(points._asdict())['y']
    
    def to_tuple(self):
        return (self.x, self.y)


class Body:
    def __init__(self, skeleton_keypoints):
        self.skeleton_keypoints = skeleton_keypoints._asdict()["joints"]
        self.parsed_keypoint = list()

    def parser(self):
        for keypoint in self.skeleton_keypoints:
            self.parsed_keypoint.append(Keypoint(keypoint).to_tuple())
        return self.parsed_keypoint


class Evaluate:
    def __init__(self, body):
        self.body = body.parser()

    def angle(self, B, A, C):
        # angle of A
        try:
            a = np.array(A)
            b = np.array(B)
            c = np.array(C)
            e1, e2 = (c-a, b-a)
            num = np.dot(e1, e2)
            denom = np.linalg.norm(e1) * np.linalg.norm(e2)
            angle = np.arccos(num/denom) * 180 / np.pi
            return int(angle)
        except Exception as e:
            return -1

    def association_point(self, key):
        return ((1, key+1) if key in [5, 8, 11] else (key-1, key+1))

    def calculate_angles(self):
        evaluate_position = [1, 2, 3, 5, 6, 8, 9, 11, 12]
        for i in evaluate_position:
            (pre, nex) = self.association_point(i)
            angle = self.angle(self.body[pre], self.body[i],self.body[nex])
            # print(angle)


if __name__ == "__main__":
    bodies = [SkeletonKeypoints(joints=[Coordinate(x=131.25, y=48.75), Coordinate(x=131.25, y=96.25), Coordinate(x=96.25, y=96.25), Coordinate(x=53.75, y=133.75), Coordinate(x=33.75, y=83.75), Coordinate(x=166.25, y=98.75), Coordinate(x=196.25, y=136.25), Coordinate(x=216.25, y=101.25), Coordinate(x=116.25, y=208.75), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=158.75, y=203.75), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=126.25, y=43.75), Coordinate(x=138.75, y=43.75), Coordinate(x=116.25, y=53.75), Coordinate(x=148.75, y=53.75)], confidences=[0.9249143600463867, 0.9447815418243408, 0.8818870186805725, 0.92684006690979, 0.8767169713973999, 0.8767545223236084, 0.8759602308273315, 0.8763948678970337, 0.5975141525268555, 0.0, 0.0, 0.6924083232879639, 0.0, 0.0, 1.0069090127944946, 0.9924660921096802, 0.9715789556503296, 0.9577101469039917], id=0)]
    # bodies = open()
    for i in bodies:
        body = Body(i)
        eva = Evaluate(body)
        eva.calculate_angles()
        # print(eva.calculate_angles())
