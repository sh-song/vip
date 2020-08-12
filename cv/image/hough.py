import cv2
import numpy as np

sample = cv2.imread('resource/sample.png')
sample = cv2.resize(sample, dsize=(1396//2, 784//2), interpolation=cv2.INTER_AREA)

top_sample = sample[:253,:,:]
bottom_sample = sample[253:,:,:]


gray = cv2.cvtColor(bottom_sample, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 400, 450, apertureSize=3)

lines = cv2.HoughLines(edges, 1, np.pi/180, 100) # 마지막게 Threshold

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

        cv2.line(bottom_sample, (x1, y1), (x2, y2), (0, 0 ,255), 2)

res = np.vstack((top_sample, bottom_sample))
cv2.imshow('sample', res)

cv2.waitKey(0)
#cv2.waitKey(0)
#cv2.waitKey(0)