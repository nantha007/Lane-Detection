import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from werkzeug.formparser import _end
def least_squares(image, left_lane_hist, right_lane_hist,L_coef, R_coef):

    prev_L = [0,0,0]
    prev_L = L_coef
    prev_R = [0,0,0]
    prev_R = R_coef

    thresh = 130
    binaryImage = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    colorImage = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
    L_count = 0
    R_count = 0
    left = [[0,0]]
    right = [[0,0]]
    var = right_lane_hist - left_lane_hist
    for i in range(left_lane_hist-150,left_lane_hist+150):
        for j in range(0,image.shape[0]-1):

            if binaryImage[j,i] == 255:
                left = np.concatenate((left,[[i, j]]), axis=0)
                L_count = L_count + 1
    for i in range(right_lane_hist-150,right_lane_hist+150):
        for j in range(0,image.shape[0]-1):
            if binaryImage[j,i] == 255:
                right = np.concatenate((right,[[i, j]]), axis=0)
                R_count = R_count + 1

    left = np.delete(left, (0,1), axis =0)
    right = np.delete(right, (0,1), axis =0)

    if R_count > 200 :
        R_coef = np.polyfit(right[:,1].T,right[:,0].T,2)
    else :
        R_coef = prev_R

    if L_count> 200:
        L_coef = np.polyfit(left[:,1].T,left[:,0].T,2)
    else:
        L_coef = prev_L
    if np.absolute(R_coef[0] - L_coef[0]) > .01 or np.absolute(R_coef[1] - L_coef[1]) > 1.7 or np.absolute(R_coef[2] - L_coef[2]) > 800:
        L_coef = prev_L
        R_coef = prev_R

    L_y = np.poly1d(L_coef)
    R_y = np.poly1d(R_coef)
    L_end = L_y(719)
    R_end = R_y(719)
    if np.absolute(L_end - R_end) < 480 and np.absolute(L_end - R_end) < 520 or L_end > 600:
         L_coef = prev_L
         R_coef = prev_R

    '''
    L_y = np.poly1d(L_coef)
    R_y = np.poly1d(R_coef)
    colorImage2 = colorImage
    xp = np.linspace(0,1279, 1280)
    L_z = L_y(xp)
    R_z = R_y(xp)
    x = np.zeros(1280)
    for k in range(0,720):
       try:
           colorImage2[k,int(L_z[k])] = [0,0,255]
           colorImage2[k,int(R_z[k])] = [0,0,255]
       except:
           pass
    cv2.imshow('fit', colorImage2)
    print('L_coef:', L_coef)
    print('R_coef:', R_coef)
    '''
    #return xp,L_z,xp,R_z, L_coef, R_coef
    return L_coef, R_coef
