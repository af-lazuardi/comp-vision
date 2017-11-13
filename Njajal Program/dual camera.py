import numpy as np
import cv2
from matplotlib import pyplot as plt

camR=cv2.VideoCapture(1)
camL=cv2.VideoCapture(2)

while(True):
    retR, frameR = camR.read()
    retL, frameL = camL.read()
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Gray R',grayR)
    cv2.imshow('Gray L',grayL)


    stereo = cv2.StereoBM(cv2.STEREO_BM_BASIC_PRESET,ndisparities=16, SADWindowSize=15)
    
    disparity = stereo.compute(grayL,grayR)
    print disparity
    plt.imshow(disparity,'gray')
    plt.show()

    
    if cv2.waitKey(1) & 0xFF == ord ('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
