
from collections import namedtuple
import os
import json


Coordinate = namedtuple("Coordinate", ["x", "y"])
SkeletonKeypoints = namedtuple("SkeletonKeypoints", ["joints", "confidences", "id"])

skeletons = [SkeletonKeypoints(joints=[Coordinate(x=394.66668701171875, y=272.0), Coordinate(x=426.66668701171875, y=442.66668701171875), Coordinate(x=266.66668701171875, y=453.3333435058594), Coordinate(x=224.0, y=730.6666870117188), Coordinate(x=-1.0, y=-1.0), Coordinate(x=597.3333740234375, y=442.66668701171875), Coordinate(x=682.6666870117188, y=752.0), Coordinate(x=490.66668701171875, y=720.0), Coordinate(x=288.0, y=933.3333740234375), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=480.0, y=976.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=-1.0, y=-1.0), Coordinate(x=352.0, y=240.0), Coordinate(x=426.66668701171875, y=229.33334350585938), Coordinate(x=309.3333435058594, y=261.3333435058594), Coordinate(x=490.66668701171875, y=218.6666717529297)], confidences=[0.9431966543197632, 0.8282583951950073, 0.7755342125892639, 0.6829060912132263, 0.0, 0.8233133554458618, 0.7878410220146179, 0.840853750705719, 0.29739099740982056, 0.0, 0.0, 0.32887616753578186, 0.0, 0.0, 0.9171513319015503, 0.9690274596214294, 0.7840135097503662, 0.9125882983207703], id=0)]


skps = dict()
with open("{}/{}.json".format('skp_output', '001'), "w") as f:
    for i in skeletons:
        skps['id'] = skeletons.index(i)
        print(skps)
        # skps['skp'] = body.calculate_angles()
    
    json.dump(skps, f)