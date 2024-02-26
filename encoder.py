import cv2
import face_recognition
import pickle
import os


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceaccountkey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://faceattendencerealtime-66d5a-default-rtdb.firebaseio.com/",
    "storageBucket": "faceattendencerealtime-66d5a.appspot.com"
})


# Import studets images
folder_image_path = "image"
image_paths = os.listdir(folder_image_path)
image_list = []
id = []  # Id of the students which are the roll numbers of the students
for path in image_paths:
    image_list.append(cv2.imread(os.path.join(folder_image_path, path)))
    id.append(os.path.splitext(path)[0])

    file_name = f'{folder_image_path}/{path}'

    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_filename(file_name)
# print(id)

# Create the encodings


def find_encodings(image_list):
    encode_list = []
    for img in image_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_list.append(face_recognition.face_encodings(img)[0])

    return encode_list


print("===-Encoding started===")
encode_list_known = find_encodings(image_list)
encode_list_known_with_id = [encode_list_known, id]
print("===-Encoding finished===")

file = open("Encode_file.p", "wb")
pickle.dump(encode_list_known_with_id, file)
file.close()
print("File Saved Success")
