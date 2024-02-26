import os
import cv2
import numpy as np
import argparse
import warnings
import time
import pickle
import face_recognition

import cvzone
import sys
# some_file.py
import sys
# caution: path[0] is reserved for script path (or '' in REPL)
# sys.path.insert(1, '/Silent-Face-Anti-Spoofing-master')

# from Silent_Face_Anti_Spoofing_master import src
from test import test
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    success, img = cap.read()

    if test(image=img, model_dir="C:/Users/krishnendu/Facet/resources/anti_spoof_models", device_id=0) == 1:
        print("Real image successfully")
    else:
        print("Fake image successfully")
