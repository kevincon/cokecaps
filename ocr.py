import cv2
import numpy as np

###### MY CODE #########
All = []

HighY = [] ##create a list to store all the identified values

LowY = []

highY = 0
highX = 0
#######   training part    ############### 
samples = np.loadtxt('generalsamples.data',np.float32)
responses = np.loadtxt('generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.KNearest()
model.train(samples,responses)

############################# testing part  #########################
#gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
#cv2.imshow('normal', gray)
#cv2.waitKey(0)
#blur = cv2.GaussianBlur(gray,(5,5),5)
#cv2.imshow('normal', blur)
#cv2.waitKey(0)
#thresh = cv2.adaptiveThreshold(blur,255,0,1,13,2)

im = cv2.imread('photoBooth.jpg')
out = np.zeros(im.shape,np.uint8)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),5)
thresh = cv2.adaptiveThreshold(blur,255,0,1,15,2)
#thresh = cv2.adaptiveThreshold(gray,255,0,1,13,2)

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt)>400:
        [x,y,w,h] = cv2.boundingRect(cnt)
        ##print 'X AND Y'
        
        #print "x = %d and y = %d" % (x,y)
        if  h>28:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.find_nearest(roismall, k = 1)
            string = str(int((results[0][0])))
      #      if y < 100:
       #         print "%d and y = %d and string = %s" % (x,y,string)
            if y>highY+100: #update highest Y
                highY = y
            if x>highX+50:
                highX = x
            All.append((string,x,y))
            ##print string
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

#print "HIGHY = %s" % (highY)
#print "HIGHX = %s" % (highX)

for el in All: ####sort them into high Y and low Y
    if el[2]>highY-100 and el[2]<highY+100:
        HighY.append(el)
    else:
        LowY.append(el)

code = '' 

LowY.sort(key=lambda x: x[1])
while len(LowY) !=0: ##process top row
    element = LowY.pop(0)
    code = code + chr(int(element[0]))
    #print "ASCII = %c" % (chr(int(element[0])))

HighY.sort(key=lambda x: x[1])
while len(HighY) !=0: ##process bot row
    element = HighY.pop(0)
    code = code + chr(int(element[0]))
    #print "ASCII = %c" % (chr(int(element[0])))
print "Your code is: %s" % (code)

cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)
