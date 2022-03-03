# 检测机械臂平行时二维码上侧的中心,记录下来,然后再测位移后的据摄像头深度,然后测出两点距离
import math

import pyrealsense2 as rs
import cv2
import numpy as np
import QRcam as myqr


if __name__ == '__main__':
    pipe = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
    config.enable_stream(rs.stream.infrared, 1024, 768, rs.format.y8, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    align_to = rs.stream.color
    align = rs.align(align_to)
    profile=pipe.start(config)
    try:
        depth1 = 0
        depth2 = 0
        img1=0
        img2=0
        camera_coordinate1=0
        camera_coordinate2=0

        while True:
            frame = align.process(pipe.wait_for_frames())
            depth_frame = frame.get_depth_frame()
            color_frame = frame.get_color_frame()
            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            if not depth_frame or not color_frame:
                continue
            four_point, image = myqr.QR_getter(np.asanyarray(color_frame.get_data()))
            cv2.imshow('1', image)
            if four_point is None:
                continue
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                point_x = int((four_point[0, 3, 0] + four_point[0, 2, 0]) // 2)
                point_y = int((four_point[0, 3, 1] + four_point[0, 2, 1]) // 2)
                depth = depth_frame.get_distance(point_x, point_y)
                depth1 = depth
                camera_coordinate1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [point_x, point_y], depth)
                # （x, y)点在相机坐标系下的真实值，为一个三维向量。其中camera_coordinate[2]仍为dis，camera_coordinate[0]和camera_coordinate[1]为相机坐标系下的xy真实距离。
                print('dep1',depth1)
                cv2.destroyAllWindows()
                break

        while True:
            frame = align.process(pipe.wait_for_frames())
            depth_frame = frame.get_depth_frame()
            color_frame = frame.get_color_frame()
            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            if not depth_frame or not color_frame:
                continue
            four_point, image = myqr.QR_getter(np.asanyarray(color_frame.get_data()))
            cv2.imshow('2', image)
            if four_point is None:
                continue

            key = cv2.waitKey(1)
            if key & 0xFF == ord('q') or key == 27:
                point_x = int(four_point[0, 3, 0] + four_point[0, 2, 0]) // 2
                point_y = int(four_point[0, 3, 1] + four_point[0, 2, 1]) // 2
                depth = depth_frame.get_distance(point_x, point_y)
                depth2 = depth
                camera_coordinate2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [point_x, point_y], depth)
                # （x, y)点在相机坐标系下的真实值，为一个三维向量。其中camera_coordinate[2]仍为dis，camera_coordinate[0]和camera_coordinate[1]为相机坐标系下的xy真实距离。
                cv2.destroyAllWindows()
                break
        print('oooooooooooooo',camera_coordinate1)
        dis_coordinate=math.sqrt((camera_coordinate1[0]*100-camera_coordinate2[0]*100)**2+(camera_coordinate1[1]*100-camera_coordinate2[1]*100)**2+(camera_coordinate1[2]*100-camera_coordinate2[2]*100)**2)
        print(dis_coordinate)
    finally:

        pipe.stop()

