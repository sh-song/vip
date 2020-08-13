# 일단 지금까지 배운걸로만 해봤음.

import cv2
import numpy as np
cap = cv2.VideoCapture('resource/project_video.mp4')


ret, frame = cap.read()
top_frame = frame[:470,:,:]
vmid_frame = frame[470:662,:,:]
bot_frame = frame[662:,:,:]

gray = cv2.cvtColor(vmid_frame, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 200, 300)
lines = cv2.HoughLines(edges, 1, np.pi/180, 100) # 마지막게 Threshold

#<class 'numpy.ndarray'>
print(type(frame))
print(type(edges))
print(type(lines))
#