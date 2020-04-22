import numpy as np
import random

x = random.randint(0, 255)

skeleton_color = tuple(list(np.random.choice(range(1, 256), size=3)))
# skeleton_color = np.random.randint(256, size=3).tolist()
color = (100, 254, 213)
print(skeleton_color, color)
print(type(skeleton_color), type(color))
print(type(skeleton_color[0]), type(color[0]))

# import random
# limit = random.randint(1, 11)
# count = 0
# while count < limit:
#     print('A', end=" ")
#     count += 1
