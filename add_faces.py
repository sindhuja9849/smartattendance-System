import cv2
import pickle
import numpy as np
import os

# Initialize video capture and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0
names=[]
name = input("Enter Your Name: ")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50))

        # Collect face images at intervals
        if len(faces_data) < 100 and i % 10 == 0:  # Collect up to 100 images
            faces_data.append(resized_img)

            # Append the name for each face captured
            if len(names) < len(faces_data):  # Ensure names list is updated
                names.append(name)

        i += 1
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

# Convert list to numpy array and reshape
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(faces_data.shape[0], -1)  # Ensure correct reshaping

# Load existing names or initialize
if os.path.exists('data/names.pkl'):
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
else:
    names = []

# Ensure the names are appended based on the number of new faces captured
if len(faces_data) > 0:
    names += [name] * len(faces_data)  # Repeat name for each new face

# Save names
with open('data/names.pkl', 'wb') as f:
    pickle.dump(names, f)

# Load existing face data or initialize
if os.path.exists('data/faces_data.pkl'):
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    faces = np.append(faces, faces_data, axis=0)  # Append new faces
else:
    faces = faces_data

# Save updated face data
with open('data/faces_data.pkl', 'wb') as f:
    pickle.dump(faces, f)

print("Script finished successfully. Captured images:", len(faces_data))
