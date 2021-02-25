# Import required packages
import cv2
import pytesseract
import time
import numpy as np
import os

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

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread("CaptureImage.jpg")

# Preprocessing the image starts
img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# img = cv2.GaussianBlur(img, (5, 5), 0)
img = cv2.medianBlur(img, 5)
# img = cv2.bilateralFilter(img,9,75,75)

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_TOZERO)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))

# Appplying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

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
    text = pytesseract.image_to_string(cropped)

    # Formatting the text

    # Appending the text into file
    result += (text + "\n")
    # file.write(text)
    # file.write("\n")

result = result.replace("  ", "")
file.write(result)


# Close the file
file.close

os.remove('CaptureImage.jpg')

def funct():
    print("Hello")
