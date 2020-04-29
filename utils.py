import numpy as np


def calculate_angle(point_a, point_b):
    """ Calculate angle between two points """
    ang_a = np.arctan2(*point_a[::-1])
    ang_b = np.arctan2(*point_b[::-1])
    return np.rad2deg((ang_a - ang_b) % (2 * np.pi))

a = np.array([14, 140])
b = np.array([13, 120])
c = np.array([12, 130])
d = np.array([11, 110])

# create vectors
ba = a - b
bc = c - b
cd = d - c

# calculate angle
cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))

angle = np.arccos(cosine_angle)
inner_angle = np.degrees(angle)

print(inner_angle)  # 8.57299836361
print(calculate_angle(bc, cd)) # 188.572998364
print(calculate_angle(cd, bc)) # 171.427001636