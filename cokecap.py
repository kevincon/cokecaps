import cv2
import threading
import sys
from train import *
from constants import *

train = False
lock = threading.Lock()
timer = None
stop_timer = False

# Start overlay variables
ocr_boxes = []

# End overlay variables

for arg in sys.argv:
    if arg == 'train':
        train = True
        break

frame = None
ocr = CokeOCR(train)


def draw_overlays():
    #print boxes
    for box in ocr_boxes:
        [x, y, w, h] = box
        cv2.rectangle(frame, (TARGET_RECTANGLE_X + x, TARGET_RECTANGLE_Y + y), (TARGET_RECTANGLE_X + x + w, TARGET_RECTANGLE_Y + y + h), (0, 255, 0), 2)


def rect_from_center(image, (X, Y), width, height, (B, G, R)):
    cv2.rectangle(image, (X - width / 2, Y - height / 2), (X + width / 2, Y + height / 2), (B, G, R), 2)
    cv2.circle(image, (X, Y), TARGET_CIRCLE_RADIUS, (B, G, R), 2)


def take_picture():
    lock.acquire()
    global ocr_boxes
    ocr_boxes = ocr.ocr(frame)
    print "take picture!"
    if not stop_timer:
        timer = threading.Timer(3, take_picture)
        timer.start()
    lock.release()


cv2.namedWindow("VideoWindow")
webcam = cv2.VideoCapture(0)

if webcam.isOpened():  # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False

if not train:
    timer = threading.Timer(3, take_picture)
    timer.start()

while rval:
    lock.acquire()
    draw_overlays()
    rect_from_center(frame, (CENTER_X, CENTER_Y), TARGET_RECTANGLE_WIDTH, TARGET_RECTANGLE_HEIGHT, (0, 0, 200))
    cv2.imshow("VideoWindow", frame)
    rval, frame = webcam.read()
    lock.release()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        if train:
            ocr.publish()
        break

    if train and key == 32:
            lock.acquire()
            ocr.analyze(frame)
            lock.release()

stop_timer = True
