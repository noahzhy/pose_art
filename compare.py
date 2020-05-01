import os
import numpy as np
import time



def compare_skps_angles(user, standard, error_rate):
    """
    1. user angles, 2. standard angles answer, 3. error rate
    """
    without_empty = list()
    correct_score = 0

    for x, y in zip(user, standard):
        if not (x < 0 or y < 0):
            without_empty.append(abs(x-y))

    for i in without_empty:
        if i < error_rate:
            correct_score += int(100 / len(without_empty))

    return correct_score


if __name__ == "__main__":
    # user = [81, 114, -1, 71, 97, 34, -1, 18, -1]
    user = [81, 110, -1, 100, 72, 34, -1, 18, -1]
    standard = [83, 102, 25, 105, 65, 29, -1, 19, -1]

    print(compare_skps_angles(user, standard, 10))