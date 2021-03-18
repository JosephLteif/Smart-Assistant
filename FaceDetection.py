# imports
import numpy as np
import cv2
import os
import face_recognition


def funct():
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_smile.xml')
    side_face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_profileface.xml')

    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    font = cv2.FONT_HERSHEY_SIMPLEX
    i = 0
    Joseph_encoding = face_recognition.face_encodings(face_recognition.load_image_file("../Image for python FD/FaceImage0.jpg"))[0]
    while True:
        if i > 3:
            i = 0

        # check returns true if python can actually read and frame is ndim numpy array
        check, frame = video.read()
        frame = np.fliplr(frame).copy()
        # frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        cv2.imwrite("VideoCapture.jpg", frame)

        image = cv2.imread("VideoCapture.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if i == 0:
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            sidefaces = side_face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            image = cv2.rectangle(
                image, (x, y), (x+w, y+h), (255, 255, 255), 2)            
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            if i == 0:
                smiles = smile_cascade.detectMultiScale(roi_gray, 1.3, 43)
                encodings1 = face_recognition.face_encodings(image, faces)[0]
            for (ex, ey, ew, eh) in smiles:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (255, 255, 255), 2)
            print(face_recognition.face_distance([encodings1],Joseph_encoding))
            if(face_recognition.face_distance([encodings1],Joseph_encoding)<0.62):
                Name = "Joseph Lteif"
            else:
                Name = "UnKnown"
            print(Name)
            if len(smiles):
                State = '{} - Happy'.format(Name)
            else:
                State = '{} - Neutral'.format(Name)
            cv2.putText(image, State, (x, y+h+20), font, 0.5,
                        (255, 255, 255))  # ---write the text

        for (x, y, w, h) in sidefaces:
            State = 'UnKnown - Neutral'
            image = cv2.rectangle(
                image, (x, y), (x+w, y+h), (255, 255, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.3, 43)
            for (ex, ey, ew, eh) in smiles:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (255, 255, 255), 2)
            if len(smiles):
                State = 'Unknown - Happy'
            cv2.putText(image, State, (x, y+h+20), font, 0.5,
                        (255, 255, 255))  # ---write the text

        if len(faces) == 0 and len(sidefaces) == 0:

            cv2.imshow('img', frame)
            Key = cv2.waitKey(1)
        else:
            cv2.imshow('img', image)
            Key = cv2.waitKey(1)
        if Key == ord('q'):
            break
        # print("Found {0} Faces!".format(len(faces)))
        i = i + 1
    os.remove('VideoCapture.jpg')


funct()
