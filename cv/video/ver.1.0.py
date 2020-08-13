# 일단 지금까지 배운걸로만 해봤음.

import cv2
import numpy as np
cap = cv2.VideoCapture('resource/project_video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    top_frame = frame[:470,:,:]
    vmid_frame = frame[470:662,:,:]
    bot_frame = frame[662:,:,:]

    gray = cv2.cvtColor(vmid_frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 200, 300)
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

            cv2.line(vmid_frame, (x1, y1), (x2, y2), (0, 0 ,255), 2)
            result = np.vstack((top_frame, vmid_frame, bot_frame))


    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()