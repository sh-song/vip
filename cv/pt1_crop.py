# 사진에 동그라미 그리고 1/4로 잘라서 검게 채우기

import cv2
sample = cv2.imread('cv/dang.png') # relative path
height, width, rgb = sample.shape
print(height, width, rgb)
#544 776 3
cv2.circle(sample, (width//2, height//2), 100, (0, 0, 255), 10)

crop_sample = sample[:height//2,:width//2,:]

crop_sample[:,:,:] = 0

cv2.imshow('original', sample)
cv2.imshow('croped', crop_sample)
cv2.waitKey(0)