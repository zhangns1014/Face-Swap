'''
Filename: getLandmarks.py
Author: Zheyuan Xie
Date created: 2018-12-18
'''

import dlib
import numpy as np
from PythonSDK.facepp import API,File
from pprint import pformat
import cv2

# dlib detector and predictor
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)

# faceplusplus API and landmark notation
api = API()
f = open('landmark83.txt')
landmark_name = f.readline().split(',')
f.close()

def get_landmarks(im):
    rects = detector(im, 1)
    if len(rects) is not 1:     # if no face or multiple faces, return None
        return None
    return np.array([[p.x, p.y] for p in predictor(im, rects[0]).parts()])

def get_landmarks_facepp(img):
    cv2.imwrite('temp.jpg',img)
    res = api.detect(image_file=File('./temp.jpg'), return_landmark=1)
    lm = np.zeros((83,2))
    for i in range(83):
        point = res['faces'][0]['landmark'][landmark_name[i]]
        lm[i,0] = point['x']
        lm[i,1] = point['y']
    return lm

if __name__ == "__main__":
    from loader import loadvideo
    filename1 = 'CIS581Project4PartCDatasets/Easy/FrankUnderwood.mp4'
    print('loading...')
    video = loadvideo(filename1)
    print('done')
    img = video[0]
    lm = get_landmarks_facepp(img)
    for groups in lm:
        cv2.circle(img, (int(groups[0]),int(groups[1])), 3, (255, 0, 0), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)