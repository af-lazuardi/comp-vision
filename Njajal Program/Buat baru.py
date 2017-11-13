import cv2
import numpy as np
from matplotlib import pyplot as plt

im=cv2.imread('data9.bmp', cv2.WINDOW_AUTOSIZE)
cv2.imshow('image',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

