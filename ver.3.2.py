
import cv2
import numpy as np

############ Functions ###################

# 1. Cut in triangle shape
def region_of_interest(image):
    height = image.shape[0]
    triangle = np.array([[(tri_bot_left, height), (tri_bot_right, height), (focus_x, focus_y)]])
    # vertices: bottom left, bottom right, top
    mask = np.zeros_like(image) # Generate an array filled with zeros, 
                                # but in same shape and type as a given array
    cv2.fillPoly(mask, triangle, (255, 255, 255)) #Fill in the mask array with triangle array
    masked_image = cv2.bitwise_and(image, mask) # Cropped image, in triangle shape
    return masked_image

# 3. Canny
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0) # Only odd numbers
    canny = cv2.Canny(blur, 20, 120) # Threshold LOW ~ HIGH
    return canny

# 3-A. Canny_alter
def canny_alter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(gray, (9, 9), 0) # Only odd numbers
    canny = cv2.Canny(blur, 20, 120) # Threshold LOW ~ HIGH
    return canny

# 5. Slope Filter
def slopeFilter(lines):
    filtered_lines = []
    not_lines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
     
            if -999 < slope < left_slope - 0.1  or  right_slope +0.02 < slope < 999 : # left -- right

                filtered_lines.append(line)
            else:
                not_lines.append(line)

    return filtered_lines

# 6. Display lines
def display_lines(image, lines):
    line_image = np.zeros_like(image) # Array filled with zeros. now empty

    if lines is not None:
        for line in lines:
            try:
                x1, y1, x2, y2 = line # define coordinates
            except:
                x1, y1, x2, y2 = line[0] # if there's no line detected


            cv2.line(line_image, (x2, y2), (x1, y1), (0, 255, 0), 5) #last parameter = thickness
            # Fill the empty array with the lines
        return line_image
            
###########################################################
###########################################################

cap = cv2.VideoCapture('resource/project_video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    # 0. Import image and Create background
    img = frame
    background = np.copy(img)

    ## detect alter
    alter = 0 # pave = black <=> value Red < 100
    if img[570, 553, 2] > 100:
        alter = 1
        print('ALTER')
    
    # 1. Cut in triangle shape
    tri_bot_left, tri_bot_right = 0, 1279
    focus_x, focus_y = 644, 425
    left_slope = (718 - focus_y) / (tri_bot_left - focus_x)
    right_slope = (718 - focus_y) / (tri_bot_right - focus_x)

    roi = region_of_interest(img)

    # 2. Cut in half
    left_roi = roi[:, :focus_x, :]
    right_roi = roi[:, focus_x:, :]

    # 3. Canny
    if alter == 0: 
        left_canny_roi = canny(left_roi)
        right_canny_roi = canny(right_roi)

    else:
        left_canny_roi = canny_alter(left_roi)
        right_canny_roi = canny_alter(right_roi)


    # 4. Detect lines by hough
    left_lines = cv2.HoughLinesP(left_canny_roi, 2, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=10)
    right_lines = cv2.HoughLinesP(right_canny_roi, 2, np.pi/180, 60, np.array([]), minLineLength=10, maxLineGap=200)

    left_lines_alter = cv2.HoughLinesP(left_canny_roi, 2, np.pi/180, 100, np.array([]), minLineLength=50, maxLineGap=10)
    right_lines_alter = cv2.HoughLinesP(right_canny_roi, 2, np.pi/180, 120, np.array([]), minLineLength=10, maxLineGap=150)

    # 5. slopeFilter
    filtered_left_lines = slopeFilter(left_lines)
    filtered_right_lines = slopeFilter(right_lines)

    filtered_left_lines_alter = slopeFilter(left_lines_alter)
    filtered_right_lines_alter = slopeFilter(right_lines_alter)

    # 6. Display lines
    if alter == 0 : # value Red < 100
        left_line_image = display_lines(left_roi, filtered_left_lines)
        right_line_image = display_lines(right_roi, filtered_right_lines)

    else:
        left_line_image = display_lines(left_roi, filtered_left_lines_alter)
        right_line_image = display_lines(right_roi, filtered_right_lines_alter)


    # 7. Merge the left and the right
    merged_line_image = np.hstack((left_line_image, right_line_image))

    # 8. Integrate the background with the lines image
    final_image = cv2.addWeighted(background, 0.8, merged_line_image, 1, 1)

    # 9. Project
    cv2.imshow('result', final_image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
