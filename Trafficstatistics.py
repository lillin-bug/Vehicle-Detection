import sys

import PIL
import numpy as np
import cv2 as cv
import cv2
import time
import os

from PIL import ImageDraw
from PIL import Image
from PIL import ImageFont

from model.yolo_model import YOLO
import HyperLPRLite as pr
from demo import drawRectBox
from Vehicleidf import process_image, get_classes, draw
from MainUI import MainWindow

def detect_image(image, yolo, all_classes, count_up, count_down, boxes1, classes1, scores1):
    """Use yolo v3 to detect images.

    # Argument:
        image: original image.
        yolo: YOLO, yolo model.
        all_classes: all classes name.

    # Returns:
        image: processed image.
    """
    pimage = process_image(image)

    start = time.time()
    boxes, classes, scores = yolo.predict(pimage, image.shape)
    end = time.time()

    print('time: {0:.2f}s'.format(end - start))

    if boxes is not None:
        draw(image, boxes, scores, classes, all_classes)
        image,count_up, count_down = draw1(image, boxes, scores, classes, all_classes, count_up, count_down, boxes1, classes1, scores1)


    return image, count_up, count_down, boxes, classes, scores

def detect_video(video, yolo, all_classes):
    """Use yolo v3 to detect video.

    # Argument:
        video: video file.
        yolo: YOLO, yolo model.
        all_classes: all classes name.
    """
    video_path = os.path.join(video)
    if (os.path.exists(video_path) and video != ''):
        camera = cv2.VideoCapture(video_path)
    else:
        camera = cv2.VideoCapture(0)
        video = 'your_camera.mp4'
    res, frame = camera.read()
    if not res:
        print("file open failed and camera can not open")
    cv2.namedWindow("detection", 0)#cv2.WINDOW_AUTOSIZE
    # Prepare for saving the detected video
    sz = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*'mpeg')

    vout = cv2.VideoWriter()
    vout.open(os.path.join("videos", "res", video), fourcc, 20, sz, True)
    count_up = 0
    count_down = 0

    success, image = camera.read()
    n = 1
    while n < 2:
        success, image = camera.read()
        n += 1


    pimage = process_image(image)
    boxes, classes, scores = yolo.predict(pimage, image.shape)
    while True:
        res, frame = camera.read()

        if not res:
            break
        boxes1 = boxes
        classes1 = classes
        scores1 = scores
        image, count_up, count_down, boxes, classes, scores = detect_image(frame, yolo, all_classes, count_up, count_down, boxes1, classes1, scores1)
        model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
        for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(image):
            if confidence > 0.7:
                image = drawRectBox(image, rect, pstr + "confidence" + str(round(confidence, 3)))
                #print("plate_str:")
                #print(pstr)
                #print("plate_confidence")
                #print(confidence)

        cv2.namedWindow("detection" ,0)
        cv2.resizeWindow("detection",1000,650)
        cv2.imshow("detection", image)
        cv2.moveWindow("detection",480,180)

        # Save the video frame by frame
        vout.write(image)

        if cv2.waitKey(60) & 0xff == 27:       #按ESC退出
                break



    vout.release()
    camera.release()
def draw1(image, boxes, scores, classes, all_classes, count_up, count_down, boxes1, classes1, scores1):
    cv.line(image, (0, 700), (1920, 700), (0, 255, 0), 1)
    cv.line(image, (0, 350), (1920, 350), (0, 255, 0), 2)
    cv.putText(image, "down:" + str(count_down), (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv.putText(image, "up:" + str(count_up), (100, 100), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    cv.putText(image, str(count_up+count_down), (320, 640), cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    pilimg = Image.fromarray(image)
    draw = PIL.ImageDraw.Draw(pilimg)
    font = ImageFont.truetype("./Font/platech.ttf", 40, 0, encoding="utf-8")
    draw.text((0, 500), "输出信息,", (255, 255, 255), font=font)
    draw.text((0, 600), "此路口车流量为：", (255, 255, 255), font=font)
    image = np.array(pilimg)
    for box, score, cl in zip(boxes, scores, classes):
        if ((all_classes[cl] == 'car' or all_classes[cl] == 'bus') and score >= 0.7):
            x, y, w, h = box
            top = max(0, np.floor(x + 0.5).astype(int))
            left = max(0, np.floor(y + 0.5).astype(int))
            right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
            bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))
            # 绘制
            width = int(right - left)
            height = int(bottom - top)
            cx = int(x + (w / 2))
            cy = int(y + (h / 2))
            t1 = 100
            for box1, score1, cl1 in zip(boxes1, classes1, scores1):
                if ((all_classes[cl] == 'car' or all_classes[cl] == 'bus') and score >= 0.7):
                    x1, y1, w1, h1 = box1
                    cx1 = int(x1 + (w1 / 2))
                    cy1 = int(y1 + (h1 / 2))
                    t = abs(cx-cx1)+abs(cy-cy1)
                    if t1 > t:
                        t1 = t
                        y2 = cy1
            if (cy < 700 and y2 > 700) or cy == 700:
                count_down += 1
            if (cy > 350 and y2 < 350) or cy == 350:
                count_up += 1
            cv.circle(image, (cx, cy), 5, (0, 0, 255), 2)#image, (cx, cy), 5, (0, 0, 255), -1
            cv2.rectangle(image, (top, left), (right, bottom), (0, 0, 255), 2)
    return image, count_up, count_down
                #           (int(left) - 10, int(top) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, 8);

def main():
    yolo = YOLO(0.5, 0.5)
    file = 'data/coco_classes.txt'
    all_classes = get_classes(file)
    relative_path = MainWindow().choose()
    video = relative_path
    t = "mp4"
    p = "avi"
    if p in video !=True or t in video != True:
        detect_video(video, yolo, all_classes)