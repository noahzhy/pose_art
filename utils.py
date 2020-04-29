import numpy as np

# a = np.array([2, 2])
# b = np.array([3, 2])
# c = np.array([1, 1])
# d = np.array([2, 1])

# points = np.array([])

# A = b - a
# B = c - b
# C = a - c
# D = d - b
# print(A, B, C, D)

A = (2, 2)
B = (3, 2)
C = (2, 1)

D = (4, 3)

def angle(B, A, C):
    # angle of A
    a = np.array(A)
    b = np.array(B)
    c = np.array(C)
    e1, e2 = (c-a, b-a)
    num = np.dot(e1, e2)
    denom = np.linalg.norm(e1) * np.linalg.norm(e2)
    angle = np.arccos(num/denom) * 180 / np.pi
    return int(angle)

print(angle(A, B, D))
# print(sum(angles))