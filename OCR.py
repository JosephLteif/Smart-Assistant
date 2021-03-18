# Import required packages
import cv2
import pytesseract
import time
import numpy as np
import os
import imutils
from autocorrect import Speller
from border_crop import border_crop
from PIL import Image


def VideoOn():
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        # check returns true if python can actually read and frame is ndim numpy array
        check, frame = video.read()
        cv2.imshow('Capturing...', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            check, frame = video.read()
            a = cv2.imwrite("CaptureImage.jpg", frame)
            break

    video.release()

    cv2.destroyAllWindows()


def TesseractSetup():
    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'


def CropBorder():
    # return cropped image from which text needs to be extracted
    im = Image.open("CaptureImage.jpg")
    # im = Image.open("./Assets/quote-luck-is-when-skill-meets-opportunity-vinnie-paz-80-71-88.jpg")
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im.save("CaptureImage.jpg", dpi=(300, 300))
    # return border_crop("CaptureImage.jpg")
    return cv2.imread("CaptureImage.jpg")


def ExtractImageData(img):
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # image data
    data = pytesseract.image_to_osd(img).split()

    # Detect language
    language = data[-4]

    # Detect angle
    rotation = data[-9]
    print(rotation)
    print(data)

    # return Image Data
    return language, rotation


def PreprocessingImage(img, rotation):
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # apply rotation
    rotated = imutils.rotate(img, angle=-(int(rotation)))
    # cv2.imshow("img", rotated)
    # cv2.waitKey(0)
    # Resize the image to a given scale
    img = cv2.resize(rotated, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # Blur using GaussianBlur method
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("img", gray)
    # cv2.waitKey(0)
    # Apply threshhold
    thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)[1]
    # cv2.imshow("img", thresh1)
    # cv2.waitKey(0)
    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    # cv2.imshow("img", dilation)
    # cv2.waitKey(0)
    # Finding contours
    contours, hierarchy = cv2.findContours(
        dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()

    return im2, contours


def CreateFileToPrintTo():
    # A text file is created and flushed
    file = open("recognized.txt", "w+")
    file.write("")
    file.close()


def FindContour(im2, contours, language):
    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    result = ""
    file = open("recognized.txt", "a", encoding='utf-8')

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        if language.lower() == 'latin':
            print("Hello")
            text = pytesseract.image_to_string(cropped, lang="eng")
        else:
            text = pytesseract.image_to_string(cropped)

        # Storing the text
        result += (text + "\n")

    return result, file


def AppendResultToFile(result, file):
    spell = Speller(only_replacements=True)
    result = result.replace("  ", "")
    var = spell(result)
    file.write(var)

    # Close the file
    file.close


VideoOn()
TesseractSetup()
img = CropBorder()
language, rotation = ExtractImageData(img)
im2, contours = PreprocessingImage(img, rotation)
CreateFileToPrintTo()
result, file = FindContour(im2, contours, language)
AppendResultToFile(result, file)
os.remove('CaptureImage.jpg')
