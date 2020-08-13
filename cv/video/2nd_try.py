
import cv2
import numpy as np

def region_of_interest(image):
    img = image
    height = img.shape[0]
    width = img.shape[1]
    mask = np.zeros((height, width), dtype=np.uint8)
    points = np.array([[(195,686),(633, 415), (1131,663)]])
    cv2.fillPoly(mask, points, (255))
    res = cv2.bitwise_and(img, img, mask=mask)
    return res

cap = cv2.VideoCapture('resource/project_video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    ROI = region_of_interest(frame)
    gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 200, 300)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, 40, 5)
    
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

            cv2.line(ROI, (x1, y1), (x2, y2), (0, 0 ,255), 2)

    
    result = cv2.addWeighted(frame, 0.8, ROI, 1, 1)
    cv2.imshow('result', result)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()


