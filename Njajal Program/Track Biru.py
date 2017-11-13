import cv2
import numpy as np

def nothing(x):    
    pass
#img = np.zeros((300,200,3), np.uint8)
cv2.namedWindow('image')

cap = cv2.VideoCapture(0)


#---------Ball Ping Pong Oranye
#hlo=11 hup=70 slo=60 sup=255 vlo=200 vup=255
cv2.createTrackbar('HLo','image',4,255,nothing)
cv2.createTrackbar('HUp','image',20,255,nothing)
cv2.createTrackbar('SLo','image',144,255,nothing)
cv2.createTrackbar('SUp','image',255,255,nothing)
cv2.createTrackbar('VLo','image',126,255,nothing)
cv2.createTrackbar('VUp','image',255,255,nothing)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hlo = cv2.getTrackbarPos('HLo', 'image')
    hup = cv2.getTrackbarPos('HUp', 'image')
    slo = cv2.getTrackbarPos('SLo', 'image')
    sup = cv2.getTrackbarPos('SUp', 'image')
    vlo = cv2.getTrackbarPos('VLo', 'image')
    vup = cv2.getTrackbarPos('VUp', 'image')
    # define range of blue color in HSV
    lower_blue = np.array([hlo,slo,vlo])
    upper_blue = np.array([hup,sup,vup])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
     
    res2 = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    res2 = cv2.medianBlur(res2,15)

    #cnts = cv2.findContours(res2.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #print cnts
    #for c in cnts:
        #for g in c:
        #cv2.circle(res2,(c[0],c[1]), 2, (0,0,255),3)
        #M = cv2.moments(c)
        #cX = int (M["m10"] / M["m00"])
        #cY = int (M["m01"] / M["m00"])

        #cv2.drawContours(res,[c], -1, (0,255,0),2)
        #cv2.circle(res, (cnts[0], cnts[1]), 7, (255, 0, 0), -1)
        



#---------------- hough circle belum jadi
    #bunderan = cv2.HoughCircles(res2,cv2.cv.CV_HOUGH_GRADIENT,1,20,param1=90,param2=20, minRadius=0, maxRadius=0)
    
    #print bunderan
   
    
    #cv2.circle(res2,(bunderan[0], bunderan[1]), bunderan[2], (0,255,0),2)

    #cv2.circle(res2,(i[0],i[1]), 2, (0,0,255),3)

#----------------------------blob -------------------------
    #detector = cv2.SimpleBlobDetector()
    #keypoints = detector.detect(res2)
    #im_with_keypoints = cv2.drawKeypoints(res2, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow("Keypoints", im_with_keypoints)

    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('res2',res2)

    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
