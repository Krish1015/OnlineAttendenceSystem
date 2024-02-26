import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime as dt

from test import test


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendencerealtime-66d5a-default-rtdb.firebaseio.com/",
    "storageBucket": "faceattendencerealtime-66d5a.appspot.com"
})


bucket = storage.bucket()


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


imgbackground = cv2.imread("Resource/background.png")

folder_modes_path = "Resource/Modes"
mode_paths = os.listdir(folder_modes_path)
mode_list = []
for path in mode_paths:
    mode_list.append(cv2.imread(os.path.join(folder_modes_path, path)))

# print(len(mode_list))

# Load the encoding file
print("Loding the encoding file")
file = open('Encode_file.p', "rb")
encode_list_known_with_id = pickle.load(file)
file.close()
encode_list_known, id = encode_list_known_with_id
print("Enocode file Loaded")


mode_type = 0
counter = 0
img_student = []

while True:
    success, img = cap.read()

    # Resize image
    img_resized = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_resized = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

    face_curr_frame = face_recognition.face_locations(img_resized)
    encode_curr_frame = face_recognition.face_encodings(
        img_resized, face_curr_frame)

    imgbackground[162:162+480, 55:55+640] = img
    imgbackground[44:44+633, 808:808+414] = mode_list[mode_type]

    if face_curr_frame:
        if test(image=img, model_dir="C:/Users/krishnendu/Facet/resources/anti_spoof_models", device_id=0) == 1:
            print("Real image successfully")

            for encode_face, face_loc in zip(encode_curr_frame, face_curr_frame):
                matches = face_recognition.compare_faces(
                    encode_list_known, encode_face)
                face_dist = face_recognition.face_distance(
                    encode_list_known, encode_face)
                # print("matches",matches)
                # print("face_dist",face_dist)

                match_index = np.argmin(face_dist)
                # print("Match index",match_index)

                if matches[match_index]:
                    # print("Known face is detected")
                    # print(id[match_index])
                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    bbox = 55+x1, 162+y1, x2-x1, y2-y1
                    imgbackground = cvzone.cornerRect(
                        imgbackground, bbox, rt=0)
                    curr_id = id[match_index]
                    # print(curr_id)

                    if counter == 0:
                        cvzone.putTextRect(
                            imgbackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendence", imgbackground)
                        cv2.waitKey(1)
                        counter = 1
                        mode_type = 1

            if counter != 0:

                if counter == 1:
                    # Getting th data from the storage
                    student_info = db.reference(f'Students/{curr_id}').get()
                    # print(student_info)

                    # Getting the image from the storage
                    blob = bucket.get_blob(f'image/{curr_id}.jpg')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    img_student = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    # Update data for attecndance
                    datetimeobject = dt.strptime(
                        student_info['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                    seconds_elapsed = (
                        dt.now() - datetimeobject).total_seconds()
                    if seconds_elapsed > 20:

                        ref = db.reference(f'Students/{curr_id}')
                        student_info['attendance'] += 1
                        ref.child('attendance').set(student_info['attendance'])
                        ref.child('last_attendance_time').set(
                            dt.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        mode_type = 3
                        counter = 0
                        imgbackground[44:44+633, 808:808 +
                                      414] = mode_list[mode_type]

                if mode_type != 3:

                    if 10 < counter < 20:
                        mode_type = 2

                    imgbackground[44:44+633, 808:808 +
                                  414] = mode_list[mode_type]

                    if counter <= 10:
                        cv2.putText(imgbackground, str(student_info['attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

                        cv2.putText(imgbackground, str(student_info['department']), (1006, 550),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(curr_id), (1006, 493),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgbackground, str(student_info['standings']), (910, 625),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgbackground, str(student_info['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgbackground, str(student_info['Year']), (1025, 625),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1)

                        (w, h), _ = cv2.getTextSize(
                            student_info['name'], cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
                        offset = (414 - w)//2
                        cv2.putText(imgbackground, str(student_info['name']), (808+offset, 445),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 55, 55), 1)

                        imgbackground[175:175+216, 909:909+216] = img_student

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        mode_type = 0
                        student_info = []
                        img_student = []
                        imgbackground[44:44+633, 808:808 +
                                      414] = mode_list[mode_type]

        else:
            print("Fake image Detected")
            #cvzone.putTextRect(imgbackground, "Fake Image Detected", (275, 400))
            #cv2.imshow("Face Attendence", imgbackground)
            #cv2.waitKey(1)
    else:
        mode_type = 0
        counter = 0
        imgbackground[44:44+633, 808:808+414] = mode_list[mode_type]

    # cv2.imshow("Webcam",img)
    cv2.imshow("Face Attendence", imgbackground)
    cv2.waitKey(1)
