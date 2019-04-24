#!/usr/bin/env python3

__author__ = "Nantha Kumar Sunder, Nithish Kumar, Rama Prashanth"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import sys

# This try-catch is a workaround for Python3 when used with ROS; it is not needed for most platforms
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass
import cv2
import matplotlib.pyplot as plt
import numpy as np
from homography import homographicTransform
from homography import getTransfomredImage
from undistortion import get_undistort
from colorSegmentation import colorSegmentation
from homography import superImpose
from leastSquares import least_squares
from turnDetection import detect_turn
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
def getVideoFile(usr_input):
    switcher = {
        1: 'challenge_video.mp4',
        2: 'project_video.mp4',
    }
    return switcher.get(usr_input, 'challenge_video.mp4')

def main():
    """ Main entry point of the app """
    print('in')
    usr_input = input(
        'Select the Video\n\t1. challenge_video.mp4 \n\t2. project_video.mp4 \n\nYour Choice: ')
    print(getVideoFile(int(usr_input)))
    cap = cv2.VideoCapture(getVideoFile(int(usr_input)))
    font = cv2.FONT_HERSHEY_SIMPLEX
    Xc = np.array(
        [[900, 0],
          [900, 710],
          [250, 710],
          [250, 0]])
    Xw = np.array(
        [[685, 450],
          [1090, 710],
          [220, 710],
          [595, 450]])
    font = cv2.FONT_HERSHEY_SIMPLEX
    L_coef = np.zeros(3)
    R_coef = np.zeros(3)
    l_coef_arr = list()
    r_coef_arr = list()
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width,frame_height))
    while(cap.isOpened()):
        ret, frame = cap.read()
        if frame is not None:
            frame = np.array(frame, dtype=np.uint8)
            image_shape = frame.shape
            undistorted_img = get_undistort(frame)
            segmented_image = colorSegmentation(undistorted_img)
            Homography = homographicTransform(Xw, Xc)
            transformed_image = getTransfomredImage(np.linalg.inv(Homography[0]), segmented_image, frame.shape[1],frame.shape[0])
            hist = np.sum(transformed_image, axis=0)
            left_lane_hist = np.argmax(hist[0:int(len(hist)/2)])
            right_lane_hist = np.argmax(hist[int(len(hist)/2):-1]) + int(len(hist)/2) - 1
            L_coef, R_coef = least_squares(transformed_image, left_lane_hist, right_lane_hist,L_coef, R_coef)
            frame = superImpose( L_coef, R_coef,Homography[0], undistorted_img)
            turn, l_coef_arr, r_coef_arr = detect_turn(L_coef, R_coef, image_shape, l_coef_arr, r_coef_arr)
            cv2.putText(frame,'Turn: ' +  turn ,(10,100), font, 2, (200,255,155), 2, cv2.LINE_AA)
            cv2.imshow('Lane Detection', frame)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
