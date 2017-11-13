from collections import deque
import numpy as np
import argparse
import imutils
import cv2

def nothing(x):
    pass

d=0
cv2.namedWindow('scroll')
cv2.namedWindow('Hasil Z')
L=640
capL = cv2.VideoCapture(1)
capR = cv2.VideoCapture(2)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
        help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
args = vars(ap.parse_args())

cv2.createTrackbar('HLo','scroll',4,255,nothing)
cv2.createTrackbar('HUp','scroll',20,255,nothing)
cv2.createTrackbar('SLo','scroll',144,255,nothing)
cv2.createTrackbar('SUp','scroll',255,255,nothing)
cv2.createTrackbar('VLo','scroll',126,255,nothing)
cv2.createTrackbar('VUp','scroll',255,255,nothing)

pts = deque(maxlen=args["buffer"])
pts1 = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
        camera = cv2.VideoCapture(1)
        camera1 = cv2.VideoCapture(2)

# otherwise, grab a reference to the video file
else:
        camera = cv2.VideoCapture(args["video"])
        camera1 = cv2.VideoCapture(args["video"])
        
while True:
    if args.get("video") and not grabbed:
                break

    _, imgL = capL.read()
    __,imgR = capR.read()
   

    hlo = cv2.getTrackbarPos('HLo', 'scroll')
    hup = cv2.getTrackbarPos('HUp', 'scroll')
    slo = cv2.getTrackbarPos('SLo', 'scroll')
    sup = cv2.getTrackbarPos('SUp', 'scroll')
    vlo = cv2.getTrackbarPos('VLo', 'scroll')
    vup = cv2.getTrackbarPos('VUp', 'scroll')
    
    _, imgL = capL.read()
    __,imgR = capR.read()
    
    hsvL = cv2.cvtColor(imgL, cv2.COLOR_BGR2HSV)
    hsvR = cv2.cvtColor(imgR, cv2.COLOR_BGR2HSV)

    lowIm = np.array([hlo,slo,vlo])
    upIm = np.array([hup,sup,vup])

    maskL = cv2.medianBlur(cv2.inRange(hsvL,lowIm,upIm),15)
    maskR = cv2.medianBlur(cv2.inRange(hsvR,lowIm,upIm),15)
    maskL = cv2.erode(maskL, None, iterations=2)
    maskR = cv2.erode(maskR, None, iterations=2)
    maskL = cv2.dilate(maskL, None, iterations=2)
    maskR = cv2.dilate(maskR, None, iterations=2)
    
    hL,wL = maskL.shape[:2]
    hR,wR = maskR.shape[:2]
        
    cntsL,hierL = cv2.findContours( maskL.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    tengahL=[248,0]
    if len(cntsL) > 0:
        c = max(cntsL, key=cv2.contourArea)
        ((x1, y1), radius) = cv2.minEnclosingCircle(c)
        mL = cv2.moments(c)
        areaL = mL['m00']
        if areaL == 0:
            areaL = 1
  
        centroidsL = (int (round(mL['m10']/areaL)),int(round(mL['m01']/areaL)) )
        
        cL = centroidsL
        cv2.circle(imgL,cL,5,(255,0,0),4)
        tengahL = cL
        if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(imgL, (int(x1), int(y1)), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(imgL, centroidsL, 5, (0, 0, 255), -1)
                        print ("camera1 : " "%1.2f" %x1, "%1.2f" %y1, "%1.2f" %radius)   

    cntsR,hierR = cv2.findContours( maskR.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    tengahR=[388,0]
    if len(cntsR) > 0:
        c = max(cntsR, key=cv2.contourArea)
        ((x2, y2), radius) = cv2.minEnclosingCircle(c)
        mR = cv2.moments(cntsR[0])
        areaR = mR['m00']
        if areaR == 0:
            areaR = 1
  
        centroidsR = (int (round(mR['m10']/areaR)),int(round(mR['m01']/areaR)) ) 
           
        cR = centroidsR
        cv2.circle(imgR,cR,5,(255,0,0),4)
        tengahR = cR
        if radius > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(imgR, (int(x2), int(y2)), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(imgR, centroidsR, 5, (0, 0, 255), -1)
                        print ("camera2 : " "%1.2f" %x2, "%1.2f" %y2, "%1.2f" %radius)
            
    pt1 = np.array(tengahL)
    pt2 = np.array(tengahR)

    # 1 cm = 13.75px
    skal = 40.75
    d = 4*skal
    f = 610
    L = 640

    o1 = np.array([L/2,0])
    o2 = np.array([L/2 + d,0])

    p1 = np.array([pt1[0],f])
    p2 = np.array([pt2[0]+d,f])

    # persamaan garis dari o1 ke p1
    a1 = 0-f
    b1 = -(o1[0] - p1[0])
    c1 = a1 * o1[0] + b1 * p1[0]

    # persamaan garis dari o2 ke p2
    a2 = 0-f
    b2 = -(o2[0] - p2[0])
    c2 = a2 * o2[0] + b2 * p2[0]

    y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2) 
    x = (c1 * b2 - b1 * c1) / (a1 * b2 - b1 * a2)

    #z = y-f
    z = y-f
   
    #print "z:{}".format(flo)
    
    cv2.putText(imgR, str(round(z/skal,1)),(pt1[0],pt1[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255),2)
    cv2.putText(imgL, str(round(z/skal,1)),(pt2[0],pt2[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255),2)
    cv2.imshow('Mask Kanan', maskR)
    cv2.imshow('Mask Kiri', maskL)
    cv2.imshow('Kanan', imgR)
    cv2.imshow('kiri',imgL)
        
    k = cv2.waitKey(5) 
    if k == 27:
        cv2.destroyAllWindows()
        break

        
    






