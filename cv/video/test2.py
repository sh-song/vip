import cv2
import numpy as np
sample = cv2.imread('resource/dang.png') # relative path

def region_of_interest(image):
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = np.array([[(195,686),(1131,663),(639,360)]])
    cv2.fillPoly(mask, roi_corners, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


show = region_of_interest(sample)

cv2.imshow('name', show)
cv2.waitKey(0)
