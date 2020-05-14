import numpy as np

a = np.array([1, 2])
b = np.array([1, 1])
c = np.array([2, 1])
n = np.cross(b-a, c-a)

# print(n)
def angle(B, A, C):
    # calculate the angle of A
    try:
        a = np.array(A)
        e1, e2 = (np.array(B)-a, np.array(C)-a)
        # print(e1, e2)
        # denom = np.linalg.norm(e1) * np.linalg.norm(e2)
        angle = np.cos(e1, e2) * 180 / np.pi

        return int(angle)
    except Exception as e:
        # print(e)
        return -999

# print(angle(a,b,c))
# print(angle(c,b,a))



ba = a - b
bc = c - b

cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
angle = np.arccos(cosine_angle)

# print(np.degrees(angle))


import numpy as np

def calculate_angle(a, mid_point, b):
    """ Calculate angle between two points """
    try:
        mid_a = a - mid_point
        mid_b = b - mid_point
        ang_a = np.arctan2(*mid_a[::-1])
        ang_b = np.arctan2(*mid_b[::-1])
        res = np.rad2deg((ang_a - ang_b) % (2 * np.pi))
        return res if res<180 else (180-res)
    except Exception as e:
        return -1

# create vectors


# # calculate angle
# cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))

# angle = np.arccos(cosine_angle)
# inner_angle = np.degrees(angle)

# print(inner_angle)  # 8.57299836361
# see how changing the direction changes the angle
print(calculate_angle(c,b,a)) # 188.572998364
print(calculate_angle(a,b,c)) # 171.427001636
