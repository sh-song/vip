
import cv2
import numpy as np

def region_of_interest(image):
    img = image
    mask = np.zeros(img.shape[0:2], dtype=np.uint8) # generate array with zeros 
    points = np.array([[(195,686),(633, 415), (1131,663)]]) 
    cv2.fillPoly(mask, points, 255) # fill array mask with array points
    res = cv2.bitwise_and(img, img, mask=mask)
    return res

#def region_of_interest(image):
#    height = image.shape[0]
#    triangle = np.array([[(200,height),(1100,height),(550,250)]])
#    mask = np.zeros_like(image)
#    cv2.fillPoly(mask,triangle,255)
#    masked_image = cv2.bitwise_and(image, image, mask)
#    return masked_image


def lines(image, low, high, threshold):
    img = image

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, low, high)
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold)

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

        cv2.line(img, (x1, y1), (x2, y2), (0, 0 ,255), 2)

    return img

cap = cv2.VideoCapture('resource/project_video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    ROI = region_of_interest(frame)
    left_ROI = ROI[:,:633,:]
    right_ROI = ROI[:,633:,:]

    lines(left_ROI, 200, 300, 100)
    lines(right_ROI, 300, 400, 100)

    merged_ROI = np.hstack((left_ROI, right_ROI))

    #result = cv2.addWeighted(frame, 1, merged_ROI, 1, 1)
    result = cv2.add(frame, merged_ROI)
    cv2.imshow('result', result)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()


