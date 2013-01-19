import numpy as np
import cv2
from constants import *

#im = cv2.imread('poop.png')
#im3 = im.copy()

def crop(im):
    return im[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT,TARGET_RECTANGLE_X:TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH]

def coke_ocr(im):
    cropped_im = crop(im)
    gray = cv2.cvtColor(cropped_im,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('VideoWindow', gray)
    # cv2.waitKey(0)
    blur = cv2.GaussianBlur(gray,(5,5),1)
    # cv2.imshow('VideoWindow', blur)
    # cv2.waitKey(0)
    thresh = cv2.adaptiveThreshold(blur,255,0,1,19,2)
    #thresh_im=im.copy()
    #thresh_im[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT,TARGET_RECTANGLE_X:TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH] = thresh[:,:]
    cv2.imshow('VideoWindow', thresh)
    cv2.waitKey(0)

    #################      Now finding Contours         ###################

    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_KCOS)

    samples =  np.empty((0,100))
    responses = []
    #keys = [i for i in range(48,58)]
    keys = ['B','W','P', 'F','H','K','V','M','L','N','0','R','5','T','7','6','9','X','J','4']

    for cnt in contours:
        if cv2.contourArea(cnt)>400:
    	    print(cv2.contourArea(cnt))
            [x,y,w,h] = cv2.boundingRect(cnt)

            if  h>28:
                cv2.rectangle(im,(TARGET_RECTANGLE_X+x,TARGET_RECTANGLE_Y+y),(TARGET_RECTANGLE_X+x+w,TARGET_RECTANGLE_Y+y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                cv2.imshow('VideoWindow',im)
                key = cv2.waitKey(0)

                if key == 27:
                    #sys.exit()
                    return
                elif chr(key).upper() in keys:
                    responses.append(key)
                    sample = roismall.reshape((1,100))
                    samples = np.append(samples,sample,0)

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print "training complete"

    #np.savetxt('generalsamples.data',samples)
    #np.savetxt('generalresponses.data',responses)
    #exit()
