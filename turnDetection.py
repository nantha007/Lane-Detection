#!/usr/bin/env python3

import numpy as np
import cv2
import matplotlib.pyplot as plt


def detect_turn(L_coef, R_coef, image_shape, l_coef_arr, r_coef_arr):
    l_coef_arr.append([L_coef[0]])
    r_coef_arr.append([R_coef[0]])
    if (len(l_coef_arr) >= 7):
        l_coef_arr.pop(0)
        r_coef_arr.pop(0)

    l_mean_coeff = np.mean(l_coef_arr)
    r_mean_coeff = np.mean(r_coef_arr)
    turn = 'Straight'
    if (l_mean_coeff < -0.00009) and (r_mean_coeff < -0.00009):
        turn = 'Left'
    elif (l_mean_coeff > 0.00009) and (r_mean_coeff > 0.00009):
        turn = 'Right'

    return turn, l_coef_arr, r_coef_arr
