#imports
import numpy as np
import cv2
import os

def funct():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')
    side_face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_profileface.xml')
    
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        # check returns true if python can actually read and frame is ndim numpy array
        check, frame = video.read()
        frame = np.fliplr(frame).copy()
        cv2.imwrite("VideoCapture.jpg", frame)
        
        image = cv2.imread("VideoCapture.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces):
            for (x, y, w, h) in faces:
                image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]
                cv2.putText(image,'Unknown',(x,y+h+20), font, 0.5, (255,0,0)) #---write the text
                # eyes = eye_cascade.detectMultiScale(roi_gray)
                # for (ex, ey, ew, eh) in eyes:
                #    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        else:
            sidefaces = side_face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(sidefaces):
                print("Hello!")
            for (x, y, w, h) in sidefaces:
                image = cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = image[y:y+h, x:x+w]

        if len(faces) == 0:

            cv2.imshow('img', frame)
            Key = cv2.waitKey(1)
        else:
            cv2.imshow('img', image)
            Key = cv2.waitKey(1)
        if Key == ord('q'):
            break
        # print("Found {0} Faces!".format(len(faces)))

    os.remove('VideoCapture.jpg')

funct()