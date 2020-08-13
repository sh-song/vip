import cv2
import numpy as np

cap = cv2.VideoCapture('resource/project_video')
img = cv2.imread('resource/sample.png')

# Edge Detection

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


test = canny(img)
cv2.imshow('test', test)
cv2.waitKey(0)
cv2.release()