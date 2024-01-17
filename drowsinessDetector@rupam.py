import cv2
import numpy as np
import dlib
from imutils import face_utils
import serial
import time

s = serial.Serial('COM10', 9600)
cap = cv2.VideoCapture(0)
hog_face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleep, drowsy, active = 0, 0, 0
status = ""
color = (0, 0, 0)

def blinked(a, b, c, d, e, f):
    up = np.linalg.norm(b - d) + np.linalg.norm(c - e)
    down = np.linalg.norm(a - f)
    ratio = up / (2.0 * down)

    if ratio > 0.25:
        return 2
    elif 0.21 < ratio <= 0.25:
        return 1
    else:
        return 0

def adjust_actions(left_blink, right_blink):
    global sleep, drowsy, active, status, color

    if left_blink == 0 or right_blink == 0:
        sleep += 1
        drowsy = 0
        active = 0
        if sleep > 6:
            s.write(b'a')
            time.sleep(2)
            status = "DRIVER SLEEPING !!!"
            color = (0, 0, 255)

    elif left_blink == 1 or right_blink == 1:
        sleep = 0
        active = 0
        drowsy += 1
        if drowsy > 6:
            s.write(b'a')
            time.sleep(2)
            status = " DRIVER DROWSY !"
            color = ()

    else:
        drowsy = 0
        sleep = 0
        active += 1
        if active > 6:
            s.write(b'b')
            time.sleep(2)
            status = " DRIVER ACTIVE :)"
            color = (255, 87, 51)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = hog_face_detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)
        
        left_blink = blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        adjust_actions(left_blink, right_blink)

        # Display facial landmarks
        for (x, y) in landmarks:
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()