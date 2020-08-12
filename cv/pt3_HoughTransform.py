import cv2
import numpy as np

sample = cv2.imread('resource/insung.jpeg')
sample_original = sample.copy() # 이미지를 그대로 복사하는 파이썬 내장 함수인듯.

gray = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 250, 300, apertureSize=3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 150) # 마지막게 Threshold

for i in range(len(lines)):
    for rho, theta in lines[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))

        cv2.line(sample, (x1, y1), (x2, y2), (0, 0 ,255), 2)

res = np.hstack((sample_original, sample))
cv2.imshow('sample', res)

cv2.waitKey(0)