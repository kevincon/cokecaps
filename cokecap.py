import cv2
from train import *
from constants import *

def rect_from_center(image,(X,Y),width,height, (B,G,R)):
    cv2.rectangle(image,(X-width/2,Y-height/2),(X+width/2,Y+height/2),(B,G,R),2)


cv2.namedWindow("VideoWindow")
webcam = cv2.VideoCapture(0)
print 'HELLO'
if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False

while rval:
    #cv2.rectangle(frame,(TARGET_RECTANGLE_X,TARGET_RECTANGLE_Y),(TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH,TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT),(0,0,200),2)
    #cropped = frame[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT,TARGET_RECTANGLE_X:TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH]
    rect_from_center(frame,(CENTER_X,CENTER_Y),TARGET_RECTANGLE_WIDTH,TARGET_RECTANGLE_HEIGHT,(0,0,200))
    cv2.imshow("VideoWindow", frame)
    rval, frame = webcam.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    if key == 32:
	#cv2.imwrite("poop.png",frame)
    	coke_ocr(frame)

