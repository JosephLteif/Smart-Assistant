import os
import os.path
from os import path
import cv2
import face_recognition
import numpy as np
import json
import threading

face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}
    Edit = False
    if not path.exists("./Data/faces/Data/face_Data.json"):
        open('./Data/faces/Data/face_Data.json', "w").close()
    with open('./Data/faces/Data/face_Data.json') as f:
        try:
            encoded = json.load(f)
        except:
            encoded = {}
    Keys = encoded.keys()

    for dirpath, dnames, fnames in os.walk("./Data/faces/Assets"):
        for f in fnames:
            if f.split(".")[0] not in Keys:
                Edit = True
                if f.endswith(".jpg") or f.endswith(".png"):
                    face = face_recognition.load_image_file("./Data/faces/Assets/" + f)
                    encoding = face_recognition.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding.tolist()
    if Edit:
        # Serializing json 
        json_Data = json.dumps(encoded)

        # Writing to face_Data.json
        with open("./Data/faces/Data/face_Data.json", "w") as outfile:
            outfile.write(json_Data)
    return encoded


def unknown_image_encoded(img, face_location):
    """
    encode a face given the image
    """
    return face_recognition.face_encodings(img, face_location)

def locate_Face(img):
    return face_recognition.face_locations(img)

def setup_Video():
    return cv2.VideoCapture(0)

def Get_Frame(video):
    return video.read()

def classify_face():
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    video = setup_Video()
    
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    unknown_face_encodings = []
    
    check, frame = Get_Frame(video)
    frame = np.fliplr(frame).copy()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face_locations = face_recognition.face_locations(frame)

    unknown_face_encodings = unknown_image_encoded(
            frame, face_locations)
    while True:
        
        found = False
        
        check0, frame0 = Get_Frame(video)
        check, frame = Get_Frame(video)
        frame = np.fliplr(frame).copy()
        
        gray0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        face_locations0 = face_cascade.detectMultiScale(gray0, 1.3, 5)
        face_locations1 = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(face_locations0) < len(face_locations1):
            found = True
            img = cv2.resize(frame, (0,0), fx=1,fy=1)
            face_locations1 = face_recognition.face_locations(img)
            unknown_face_encodings = unknown_image_encoded(frame, face_locations1)
        
        face_names = []
        name = ""
        for face_encoding in unknown_face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(faces_encoded, face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

        if not found:    
            for (x, y, w, h), name in zip(face_locations1, face_names):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2) 
                
                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (x, y+h),(x+w, y+h+20), (255, 0, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (x + 5, y+h + 15),font, 0.5, (255, 255, 255), 2)           

            
        # Display the resulting image
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            return face_names


classify_face()
