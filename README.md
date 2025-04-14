# Smart Attendance System Using Face Recognition

This project is a **Smart Attendance System** that automates the attendance process using **Face Recognition Technology**. The system detects and recognizes faces in real time to mark attendance for students, reducing manual work and ensuring efficient and accurate tracking.

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Technologies Used](#technologies-used)
4. [Installation](#installation)
5. [How It Works](#how-it-works)
6. [Project Files](#project-files)
7. [Future Enhancements](#future-enhancements)

## Overview
The Smart Attendance System captures student faces and uses them for automatic attendance marking. The system works by detecting faces during class hours, checking the pre-stored face data, and marking attendance in a local database. The system records attendance twice daily (morning and evening) and allows for half-day attendance if only the morning attendance is marked.

## Key Features
- **Face Recognition**: Utilizes **OpenCV** and **dlib** to detect and recognize faces from live webcam feed.
- **Real-Time Attendance Tracking**: Automatically marks attendance when a student is detected.
- **Morning & Evening Attendance**: Attendance is recorded twice a day (morning at 9 AM, evening at 3:30 PM).
- **Half-Day Attendance**: If only morning attendance is recorded, half-day attendance is marked.
- **Database Storage**: Stores attendance data in a local **SQLite** database (`att.db`).
- **Alerts and Notifications**: Sends alerts if someone attempts to mark attendance more than twice or if there are issues.
- **Graphical User Interface (GUI)**: Built using **Tkinter** for capturing photos and managing data.

## Technologies Used
- **Python**: Main programming language.
- **OpenCV**: For real-time face detection and recognition.
- **dlib**: For more accurate face recognition.
- **Tkinter**: For creating a simple GUI.
- **SQLite**: For storing attendance records and student data locally.
- **Haar Cascade**: For initial face detection.


