"""Demo for use yolo v3
"""
import os
import time
import cv2
import numpy as np
from model.yolo_model import YOLO
import HyperLPRLite as pr
from demo import drawRectBox
from MainUI import MainWindow


def process_image(img):
    """Resize, reduce and expand image.

    # Argument:
        img: original image.

    # Returns
        image: ndarray(416, 416, 3), processed image.
    """
    image = cv2.resize(img, (416, 416),
                       interpolation=cv2.INTER_CUBIC)
    image = np.array(image, dtype='float32')
    image /= 255.
    image = np.expand_dims(image, axis=0)   #(416,416,3) -> (1,416,416,3)

    return image


def get_classes(file):
    """Get classes name.

    # Argument:
        file: classes name for database.

    # Returns
        class_names: List, classes name.

    """
    with open(file) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]

    return class_names


def draw(image, boxes, scores, classes, all_classes):
    """Draw the boxes on the image.

    # Argument:
        image: original image.
        boxes: ndarray, boxes of objects.
        classes: ndarray, classes of objects.
        scores: ndarray, scores of objects.
        all_classes: all classes name.
    """
    for box, score, cl in zip(boxes, scores, classes):
        x, y, w, h = box

        top = max(0, np.floor(x + 0.5).astype(int))
        left = max(0, np.floor(y + 0.5).astype(int))
        right = min(image.shape[1], np.floor(x + w + 0.5).astype(int))
        bottom = min(image.shape[0], np.floor(y + h + 0.5).astype(int))

        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(all_classes[cl], score),
                    (top, left - 6),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 1,
                    cv2.LINE_AA)

        #print('class: {0}, score: {1:.2f}'.format(all_classes[cl], score))
        #print('box coordinate x,y,w,h: {0}'.format(box))

    #print()
    return boxes


def detect_image(image, yolo, all_classes):
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

    #print('time: {0:.2f}s'.format(end - start))

    if boxes is not None:
        draw(image, boxes, scores, classes, all_classes)

    return image


def detect_video(video, yolo, all_classes):
    """Use yolo v3 to detect video.

    # Argument:
        video: video file.
        yolo: YOLO, yolo model.
        all_classes: all classes name.
    """
    video_path = os.path.join("videos", "test", video)
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

    while True:
        res, frame = camera.read()

        if not res:
            break

        image = detect_image(frame, yolo, all_classes)
        model = pr.LPR("model/cascade.xml", "model/model12.h5", "model/ocr_plate_all_gru.h5")
        for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(image):
            if confidence > 0.7:
                image = drawRectBox(image, rect, pstr + "confidence" + str(round(confidence, 3)))
                print("plate_str:")
                print(pstr)
                print("plate_confidence")
                print(confidence)
        cv2.namedWindow("detection" ,0)
        cv2.resizeWindow("detection",1000,650)
        cv2.imshow("detection", image)
        cv2.moveWindow("detection",480,180)

        # Save the video frame by frame
        vout.write(image)

        if cv2.waitKey(60) & 0xff == 27:       #press ESC to quit
                break

    vout.release()
    camera.release()