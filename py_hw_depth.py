import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image

pipeline = rs.pipeline()
config = rs.config()
width, height = (640, 480)
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
pipeline.start(config)

f = open('test.txt', 'a')

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame: continue

        depth_image = np.fliplr(np.asanyarray(depth_frame.get_data()))
        depth_image = np.uint8(np.where((depth_image>= 100) & (depth_image<=1850), 255, 0))

        depth_image = cv2.bilateralFilter(depth_image, 9, 100, 100)

        contours, hierarchy = cv2.findContours(depth_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        # contours = contours[0]
        bg = np.zeros((height, width))
        cv2.drawContours(bg, contours, -1, 128, 5)

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', bg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    pipeline.stop()