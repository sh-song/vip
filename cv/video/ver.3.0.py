import cv2
import numpy as np


# 0. Import image and Create lane image
img = cv2.imread('resource/sample.png')
lane_image = np.copy(img)

# 1. Cut in triangle shape

focus_x = 600 # Super important parameter

def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([[(195, height), (1200, height), (focus_x, 415)]])
    # vertices: bottom left, bottom right, top
    mask = np.zeros_like(image) # Generate an array filled with zeros, 
                                # but in same shape and type as a given array
    cv2.fillPoly(mask, triangle, (255, 255, 255)) #Fill in the mask array with triangle array
    masked_image = cv2.bitwise_and(image, mask) # Cropped image, in triangle shape
    return masked_image

roi = region_of_interest(img)

# 2. Cut in half
left_roi = roi[:, :focus_x, :]
right_roi = roi[:, focus_x:, :]

# 3. Canny
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150) # LOW ~ HIGH
    return canny

left_canny_roi = canny(left_roi)
right_canny_roi = canny(right_roi)


# 4. Detect lines by hough
left_lines = cv2.HoughLinesP(left_canny_roi, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
right_lines = cv2.HoughLinesP(right_canny_roi, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)


# 5. Display lines
def display_lines(image, lines):
    line_image = np.zeros_like(image) # Array filled with zeros. now empty

    if lines is not None:
        for line in lines:
            try:
                x1, y1, x2, y2 = line # define coordinates
            except:
                x1, y1, x2, y2 = line[0] # if there's no line detected

            cv2.line(line_image, (x2, y2), (x1, y1), (0, 255, 0), 1) #last parameter = thickness
            # Fill the empty array with the lines
        return line_image

left_line_image = display_lines(left_roi, left_lines)
right_line_image = display_lines(right_roi, left_lines)

# 6. Merge the left and the right
merged_line_image = np.hstack((left_line_image, right_line_image))

# 7. Integrate the background with the lines image
final_image = cv2.addWeighted(lane_image, 0.8, merged_line_image, 1, 1)


test = final_image
cv2.imshow('test', test)

cv2.waitKey(0)



canny_image = canny(img)












