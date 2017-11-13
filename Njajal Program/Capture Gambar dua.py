import numpy as np
import cv2

camR=cv2.VideoCapture(1)
camL=cv2.VideoCapture(2)
d=0
retR,frameR = camR.read()

while (retR):
    retR,frameR = camR.read()
    retL,frameL = camL.read()
    #grayR = cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
    #grayL = cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)

    cv2.imshow('gray R', frameR)
    cv2.imshow('gray L', frameL)
    k = cv2.waitKey(0)
    if k == 27:
        cv.destroyAllWindows()
    elif k ==ord('s'):

        filenameR = "D:/Kuliah Yogi/Python/Njajal Program/imagesR/file_%d.jpg" %d
        filenameL = "imagesL/file_%d.jpg" %d
        cv2.imwrite(filenameR,frameR)
        cv2.imwrite(filenameL,frameL)
        d+=1
        cv2.destroyAllWindows()

    
