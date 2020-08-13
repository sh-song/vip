import cv2
import numpy as np

cap = cv2.VideoCapture('resource/project_video')
img = cv2.imread('resource/sample.png')

# Edge Detection

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150) # LOW ~ HIGH
    return canny


def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([[(195, height), (1131, height), (633, 415)]])
    # vertices: bottom left, bottom right, top
    mask = np.zeros_like(image) # Generate an array filled with zeros, 
                                # but in same shape and type as a given array
    cv2.fillPoly(mask, triangle, (255, 255, 255)) #Fill in the mask array with triangle array
    masked_image = cv2.bitwise_and(image, mask) # Cropped image, in triangle shape
    return masked_image


def display_lines(image, lines):
    line_image = np.zeros_like(image) # Array filled with zeros
    if lines is not None:
        for line in lines:
            try:
                x1, y1, x2, y2 = line
            except:
                x1, y1, x2, y2 = line[0]

            cv2.line(line_image, (x2, y2), (x1, y1), (0, 255, 0), 10)
            # Fill the empty array with the lines
        return line_image


lane_image = np.copy(img)

cropped_image = region_of_interest(img)
cropped_image = canny(cropped_image)

lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

result_line = []

for i in range(0, len(lines)):
        result_line.append(lines[i])


line_image = display_lines(lane_image, lines)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)


cv2.imshow('test', combo_image)
cv2.waitKey(0)
cv2.release()


