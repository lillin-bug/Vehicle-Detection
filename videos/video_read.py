
import os
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

def video_read(file_path):
    if(os.path.exists(file_path)):
        cv2_video = cv2.VideoCapture(file_path)
    else:
        cv2_video = cv2.VideoCapture(0)
    i=0
    print(cv2_video.isOpened())
    # 获得码率及尺寸

    while True:
        res, frame = cv2_video.read()
        if not res:
            break
        cv2.imshow("detection", frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cv2_video.release()

if __name__ == '__main__':
    #video_read("0")
    video_read("C:/Users/19163/PycharmProjects/untitled3/videos/test/video-02.mp4")
