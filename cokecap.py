import cv2

cv2.namedWindow("VideoWindow")
webcam = cv2.VideoCapture(0)

if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False

while rval:
    cv2.imshow("VideoWindow", frame)
    rval, frame = webcam.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break