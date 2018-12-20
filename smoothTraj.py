'''
Filename: smoothTraj.py
Author: Zheyuan Xie
Date created: 2018-12-18
'''

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

def smooth_landmark_traj(landmarks):
    # The landmarks should be continuous
    for ind in range(68):
        x = np.zeros((len(landmarks),1))
        y = np.zeros((len(landmarks),1))
        for t in range(len(landmarks)):
            if landmarks[t] is not None:
                x[t] = landmarks[t][ind,0]
                y[t] = landmarks[t][ind,1]
            else:
                x[t] = x[t-1]
                y[t] = y[t-1]
        x_filter = gaussian_filter1d(x,1,axis=0)
        y_filter = gaussian_filter1d(y,1,axis=0)
        for t in range(len(landmarks)):
            if landmarks[t] is not None:
                landmarks[t][ind,0] = x_filter[t]
                landmarks[t][ind,1] = y_filter[t]
    return landmarks

if __name__ == "__main__":
    from loader import loadlandmarks
    import matplotlib.pyplot as plt
    filename = 'Datasets/Easy/MrRobot.mp4'
    lm = loadlandmarks(filename)
    lm_smooth = smooth_landmark_traj(loadlandmarks(filename))
    x = np.zeros((len(lm),))
    y = np.zeros((len(lm),))
    x_filter = np.zeros((len(lm),))
    y_filter = np.zeros((len(lm),))
    for i in range(len(lm)):
        x[i] = lm[i][0,0]
        y[i] = lm[i][0,1]
        x_filter[i] = lm_smooth[i][0,0]
        y_filter[i] = lm_smooth[i][0,1]
    plt.figure(1)
    plt.plot(x,linewidth=2.0)
    plt.plot(x_filter,linewidth=2.0)
    plt.legend(["Detected","Filtered"])
    plt.xlabel("Frames")
    plt.ylabel("Pixel Coordinate X")
    plt.figure(2)
    plt.plot(y,linewidth=2.0)
    plt.plot(y_filter,linewidth=2.0)
    plt.legend(["Detected","Filtered"])
    plt.xlabel("Frames")
    plt.ylabel("Pixel Coordinate Y")
    plt.show()