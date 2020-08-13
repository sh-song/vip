
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
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    canny = cv2.Canny(blur, 20, 120) # LOW ~ HIGH
    return canny
# 3-B. Canny_alter
def canny_alter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    canny = cv2.Canny(blur, 20, 120) # LOW ~ HIGH
    return canny
# 4-A. Slope Filter
def slopeFilter(lines):
    filtered_lines = []
    not_lines = []

    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
     
     
            if left_slope +0.1 < slope < -0.5 or  0.5 < slope < right_slope -0.1 : # left -- right

                filtered_lines.append(line)
            else:
                not_lines.append(line)
    return filtered_lines


# 5. Display lines
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

# 5-B. Display Lines with HoughLines
def alter_display_lines(image, lines):
    line_image = np.zeros_like(image)

    if lines is not None:

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

                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0 ,255), 2)
            
            return line_image
            
###########################################################
cap = cv2.VideoCapture('resource/project_video.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    # 0. Import image and Create lane image
    img = frame
    lane_image = np.copy(img)

    # detect alter
    alter = 0 # pave = black
    if img[645, 464, 2] > 100:
        alter = 1
        print('ALTER')


    # 1. Cut in triangle shape
    tri_bot_left, tri_bot_right = 150, 1400
    focus_x, focus_y = 670, 200
    left_slope = (718 - focus_y) / (tri_bot_left - focus_x)
    right_slope = (718 - focus_y) / (tri_bot_right - focus_x)

    roi = region_of_interest(img)

    # 2. Cut in half
    left_roi = roi[:, :focus_x, :]
    right_roi = roi[:, focus_x:, :]

    # 3. Canny
    if alter == 0: # value Red < 100
        left_canny_roi = canny(left_roi)
        right_canny_roi = canny(right_roi)

        #print(img[634, 641, 2])
    else:
        left_canny_roi = canny_alter(left_roi)
        right_canny_roi = canny_alter(right_roi)

        #print('ALTER')

    # 4. Detect lines by hough
    left_lines = cv2.HoughLinesP(left_canny_roi, 2, np.pi/180, 50, np.array([]), minLineLength=20, maxLineGap=10)
    left_lines_alter = cv2.HoughLinesP(left_canny_roi, 2, np.pi/180, 100, np.array([]), minLineLength=50, maxLineGap=10)

    right_lines = cv2.HoughLinesP(right_canny_roi, 2, np.pi/180, 100, np.array([]), minLineLength=10, maxLineGap=200)
    right_lines_alter = cv2.HoughLinesP(right_canny_roi, 2, np.pi/180, 150, np.array([]), minLineLength=10, maxLineGap=150)

    #left_lines = cv2.HoughLines(left_canny_roi, 1, np.pi/180, 50)
    #right_lines = cv2.HoughLines(right_canny_roi, 1, np.pi/180, 50)


    # 4-A slopeFilter
    filtered_left_lines = slopeFilter(left_lines)
    filtered_right_lines = slopeFilter(right_lines)
    filtered_left_lines_alter = slopeFilter(left_lines_alter)
    filtered_right_lines_alter = slopeFilter(right_lines_alter)


    # 5. Display lines
    if alter == 0 : # value Red < 100
        left_line_image = display_lines(left_roi, filtered_left_lines)
        right_line_image = display_lines(right_roi, filtered_right_lines)

    else:
        left_line_image = display_lines(left_roi, filtered_left_lines_alter)
        right_line_image = display_lines(right_roi, filtered_right_lines_alter)


    #left_line_image = alter_display_lines(left_roi, left_lines)
    #right_line_image = alter_display_lines(right_roi, right_lines)


    # 6. Merge the left and the right
    merged_line_image = np.hstack((left_line_image, right_line_image))

    # 7. Integrate the background with the lines image
    final_image = cv2.addWeighted(lane_image, 0.8, merged_line_image, 1, 1)

    # 8. SHOW
    cv2.imshow('result', final_image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
