import numpy as np
import cv2
from constants import *

def detectColor(im):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    BLUE_MIN = np.array([71, 44, 18],np.uint8)
    BLUE_MAX = np.array([123, 90, 40],np.uint8)
    hsv=cv2.inRange(im, BLUE_MIN, BLUE_MAX)

    return hsv


def crop(im):
    return im[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y + TARGET_RECTANGLE_HEIGHT, TARGET_RECTANGLE_X:TARGET_RECTANGLE_X + TARGET_RECTANGLE_WIDTH]


class CokeOCR:
    def __init__(self, training_mode):
        if training_mode:
            self.samples = np.empty((0, 900))
            self.responses = []
        else:
            self.samples = np.loadtxt('generalsamples.data', np.float32)
            self.responses = np.loadtxt('generalresponses.data', np.float32)
            self.responses = self.responses.reshape((self.responses.size, 1))
            self.model = cv2.KNearest()
            self.model.train(self.samples, self.responses)

    def analyze(self, im):
        cropped = crop(im)
        #EXPERIMENTAL
        #color=detectColor(cropped)
        #cv2.imshow('VideoWindow', color)
        #cv2.waitKey(0)

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        
        thresh = cv2.adaptiveThreshold(gray,255,0,1,11,2)
        #thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)

        thresh = cv2.erode(thresh,None,iterations = 2)
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)
        
        thresh = cv2.dilate(thresh,None,iterations = 2)
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)

        thresh = cv2.erode(thresh,None,iterations = 2)
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)
        
        thresh = cv2.dilate(thresh,None,iterations = 2)
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)

        #thresh = cv2.dilate(thresh,None,iterations = 3)
        #cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)




        thresh = cv2.adaptiveThreshold(thresh, 255, 0, 1, 5, 1)
        #thresh_im=im.copy()
        #thresh_im[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT,TARGET_RECTANGLE_X:TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH] = thresh[:,:]
        cv2.imshow('VideoWindow', thresh)
        cv2.waitKey(0)

        median = cv2.medianBlur(thresh, 3)
        cv2.imshow('VideoWindow', median)
        cv2.waitKey(0)

        thresh = median.copy()

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

        for cnt in contours:
            if cv2.contourArea(cnt) > 900:
                print(cv2.contourArea(cnt))
                [x, y, w, h] = cv2.boundingRect(cnt)

                if h > 20:
                    cv2.rectangle(im, (TARGET_RECTANGLE_X + x, TARGET_RECTANGLE_Y + y), (TARGET_RECTANGLE_X + x + w, TARGET_RECTANGLE_Y + y + h), (0, 255, 0), 2)
                    roi = thresh[y:y + h, x:x + w]
                    roismall = cv2.resize(roi, (20, 45))
                    cv2.imshow('VideoWindow', im)
                    key = cv2.waitKey(0)

                    if key == 27:
                        return
                    elif chr(key).upper() in CODESET:
                        self.responses.append(key)
                        sample = roismall.reshape((1, 900))
                        self.samples = np.append(self.samples, sample, 0)

    def publish(self):
        self.responses = np.array(self.responses, np.float32)
        self.responses = self.responses.reshape((self.responses.size, 1))
        np.savetxt('generalsamples.data', self.samples)
        np.savetxt('generalresponses.data', self.responses)

    def ocr(self, im):
        i = 0
        All = []
        HighY = [] ##create a list to store all the identified values
        LowY = []
        highY = 0
        highX = 0
        out = np.zeros(im.shape, np.uint8)
        cropped = crop(im)
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray,5)
        
        thresh = cv2.adaptiveThreshold(gray,255,0,1,11,2)
        #thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
#cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)

        thresh = cv2.erode(thresh,None,iterations = 2)
#       cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)
        
        thresh = cv2.dilate(thresh,None,iterations = 2)
#       cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)

        thresh = cv2.erode(thresh,None,iterations = 2)
#       cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)
        
        thresh = cv2.dilate(thresh,None,iterations = 2)
#       cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)

        #thresh = cv2.dilate(thresh,None,iterations = 3)
        #cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)




        thresh = cv2.adaptiveThreshold(thresh, 255, 0, 1, 5, 1)
        #thresh_im=im.copy()
        #thresh_im[TARGET_RECTANGLE_Y:TARGET_RECTANGLE_Y+TARGET_RECTANGLE_HEIGHT,TARGET_RECTANGLE_X:TARGET_RECTANGLE_X+TARGET_RECTANGLE_WIDTH] = thresh[:,:]
#       cv2.imshow('VideoWindow', thresh)
        #cv2.waitKey(0)

        median = cv2.medianBlur(thresh, 3)
#       cv2.imshow('VideoWindow', median)
        #cv2.waitKey(0)

        thresh = median.copy()

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

        boxes = []

        for cnt in contours:
#           i = i+1
            if cv2.contourArea(cnt) > 1100:
                [x, y, w, h] = cv2.boundingRect(cnt)
                ##print 'X AND Y'

                #print "x = %d and y = %d and w = %d and h = %d" % (x,y,w,h)
                if h > 40:
                    i = i+1
                    roi = thresh[y:y + h, x:x + w]
                    roismall = cv2.resize(roi, (20, 45))
                    roismall = roismall.reshape((1, 900))
                    roismall = np.float32(roismall)
                    retval, results, neigh_resp, dists = self.model.find_nearest(roismall, k=1)
                    string = str(int((results[0][0])))
              #      if y < 100:
               #         print "%d and y = %d and string = %s" % (x,y,string)
                    if y > highY + 40:  # update highest Y
                        highY = y
                    if x > highX + 40:
                        highX = x
                    All.append((string, x, y))
                    ##print string
                    cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 0))
                    boxes.append([x, y, w, h])

                    #print "HIGHY = %s" % (highY)
                    #print "HIGHX = %s" % (highX)

        for el in All:  # sort them into high Y and low Y
            if el[2] > highY - 40 and el[2] < highY + 40:
                HighY.append(el)
            else:
                LowY.append(el)
		
        code = ''

        LowY.sort(key=lambda x: x[1])
        while len(LowY) != 0:  # process top row
            element = LowY.pop(0)
            code = code + chr(int(element[0]))
	#print "ASCII = %c" % (chr(int(element[0])))

        HighY.sort(key=lambda x: x[1])
        while len(HighY) != 0:  # process bot row
            element = HighY.pop(0)
            code = code + chr(int(element[0]))
            #print "ASCII = %c" % (chr(int(element[0])))
        if i < 14+2 and i > 14-2:
            print "Your code is: %s" % (code)
        return boxes

