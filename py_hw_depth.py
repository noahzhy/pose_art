import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()
width, height = (640, 480)
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, 30)
pipeline.start(config)

try:
    while True:
        bg = np.zeros((height, width))
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame: continue
        depth_image = np.fliplr(np.asanyarray(depth_frame.get_data()))
        depth_image = np.uint8(np.where((depth_image>= 100) & (depth_image<=1500), 255, 0))
        depth_image = cv2.bilateralFilter(depth_image, 9, 100, 100)

        # kernel = np.ones((5,5),np.uint8)
        # depth_image = cv2.morphologyEx(depth_image, cv2.MORPH_CLOSE, kernel, 3)

        contours, hierarchy = cv2.findContours(depth_image, cv2.RETR_TREE, 1)
        cv2.drawContours(bg, contours, -1, 256, 5)
        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', bg)
        print(bg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

finally:
    pipeline.stop()