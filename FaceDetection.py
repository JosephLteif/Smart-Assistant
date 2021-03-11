#imports
import numpy as np
import cv2
import os

def funct():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    img = None
    while True:
        # check returns true if python can actually read and frame is ndim numpy array
        check, frame = video.read()
        cv2.imwrite("VideoCapture.jpg", frame)
        
        image = cv2.imread("VideoCapture.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        img = cv2.imread("VideoCapture.jpg")
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
               cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
            
        if len(faces) == 0:

            cv2.imshow('img', np.fliplr(frame))
            Key = cv2.waitKey(1)
        else:
            cv2.imshow('img', np.fliplr(img))
            Key = cv2.waitKey(1)
        if Key == ord('q'):
            break
        print("Found {0} Faces!".format(len(faces)))

    os.remove('VideoCapture.jpg')

funct()