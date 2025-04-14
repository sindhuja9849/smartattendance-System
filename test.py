from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Initialize video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load model and labels
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)

with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

# Ensure that the number of samples matches the number of labels
if FACES.shape[0] != len(LABELS):
    print(f"Mismatch found: FACES has {FACES.shape[0]} samples, but LABELS has {len(LABELS)} labels.")
    exit()  # Exit the program if there is a mismatch

# Initialize KNN model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load the background image
imgBackground = cv2.imread("background.png")  # Ensure the correct path
if imgBackground is None:
    print("Error: background.png not loaded. Check the file path.")
    exit()  # Exit if the image is not loaded

COL_NAMES = ['NAME', 'TIME']

# Create Attendance directory if it does not exist
if not os.path.exists("Attendance"):
    os.makedirs("Attendance")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    attendance = []  # Initialize attendance list

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        attendance.append([str(output[0]), str(timestamp)])  # Collect attendance data

    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)
    if k == ord('o'):
        speak("Attendance Taken..")
        print("Attendance Taken..")  # Confirmation message in terminal
        time.sleep(5)

        if attendance:
            date = datetime.now().strftime("%d-%m-%Y")
            attendance_file_path = f"Attendance/Attendance_{date}.csv"
            exist = os.path.isfile(attendance_file_path)

            try:
                with open(attendance_file_path, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    if not exist:  # If file doesn't exist, write header
                        writer.writerow(COL_NAMES)
                    writer.writerows(attendance)  # Write attendance data
                    print("Attendance recorded successfully.")
            except Exception as e:
                print("Error writing to CSV:", e)

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
