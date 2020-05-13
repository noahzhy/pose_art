import json
import random
import numpy as np

from collections import namedtuple
from typing import Sequence
from collections import namedtuple
from json import JSONEncoder
from scipy import stats
# from utils import *


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

class Keypoint:
    def __init__(self, points):
        self.x = dict(points._asdict())['x']
        self.y = dict(points._asdict())['y']
    
    def to_tuple(self):
        return (round(self.x, 2), round(self.y, 2))


class Body:
    def __init__(self, body=None):
        self.body = body._asdict()["joints"]
        self.head_coordinates = Keypoint(self.body[0]).to_tuple()

    def set_body(self, body):
        self.body = body._asdict()["joints"]
        self.head_coordinates = Keypoint(self.body[0]).to_tuple()

    def get_head_coordinates(self):
        return self.head_coordinates

    # def parser(self):
    #     for keypoint in self.body:
    #         self.parsed_keypoint.append(Keypoint(keypoint).to_tuple())
    #     return self.parsed_keypoint

    def angle(self, B, A, C):
        # calculate the angle of A
        try:
            a = np.array(A)
            e1, e2 = (np.array(C)-a, np.array(B)-a)
            denom = np.linalg.norm(e1) * np.linalg.norm(e2)
            angle = np.arccos(np.dot(e1, e2)/denom) * 180 / np.pi

            return int(angle)
        except Exception as e:
            return -1

    def association_point(self, key):
        return ((1, key+1) if key in [5, 8, 11] else (key-1, key+1))

    def calculate_angles(self):
        angles_list = list()
        evaluate_position = [1, 2, 3, 5, 6, 8, 9, 11, 12]
        for i in evaluate_position:
            (pre, nex) = self.association_point(i)
            # calculate the angles with those three points
            angle = self.angle(self.body[pre], self.body[i], self.body[nex])
            angles_list.append(angle)
        return angles_list

    # def compare_skps_angles(self, error_rate, standard):
    #     """
    #     1. error rate, 2. standard angles answer, 3. user angles
    #     """
    #     num_detected_keypoints = int(len([i for i in standard if i>0])/2)+1
    #     correct_score = 0
    #     without_empty = list()

    #     for (x, y) in zip(self.calculate_angles(), standard):
    #         if not (x < 0 or y < 0):
    #             error = abs(x-y)
    #             if error <= error_rate:
    #                 without_empty.append(error_rate-error)

    #     if len(without_empty) <= num_detected_keypoints:
    #         return random.randint(11, 21)/100
    #     # calculate the correct rate, ps: get score / total score
    #     return sum(without_empty)/(len(without_empty)*error_rate)

    def compare_skps_angles(self, standard_ans):
        """
        1. error rate, 2. standard angles answer, 3. user angles
        """
        # num_detected_keypoints = int(len([i for i in standard_ans if i>0])/2)+1
        # correct_score = 0
        users, standard = list(), list()

        for (x, y) in zip(self.calculate_angles(), standard_ans):
            if not (x < 0 or y < 0):
                users.append(x)
                standard.append(y)

        if len(users) <= int(len(standard)/2)+1:
            return random.randint(11, 21)/100
        # calculate the correct rate
        return round(stats.pearsonr(users, standard)[0], 2)


if __name__ == "__main__":
    # only for testing
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

    for i in bodies:
        body = Body(i)
        # body.set_body()
        print(body.calculate_angles())
    #     print(body.get_head_coordinates())
    # compare_multi_users()
    pass
