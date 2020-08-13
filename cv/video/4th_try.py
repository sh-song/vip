import cv2
import numpy as np

cap = cv2.VideoCapture('resource/project_video.mp4')
#img = cv2.imread('resource/sample.png')

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


global_left_fit_average = []
global_right_fit_average = []

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    non_fit = []
    global global_left_fit_average
    global global_right_fit_average

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            #x1, y1, x2, y2 = np.reshape(line, (1, 4))
        
            slope = ((y1 - y2) / (x1 - x2))

            intercept = y1 - slope * x1

            if slope < 0:
                left_fit.append((slope, intercept))

            elif slope > 0:
                right_fit.append((slope, intercept))
            
            else:
                non_fit.append((slope, intercept))

    if (len(left_fit) == 0):
        left_fit_average = global_left_fit_average
    else:
        left_fit_average = np.average(left_fit, axis=0)
        global_left_fit_average = left_fit_average


    if (len(right_fit) == 0):
        right_fit_average = global_right_fit_average
    else:
        right_fit_average = np.average(right_fit, axis=0)
        global_right_fit_average = right_fit_average

    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)

    lines = [left_line, right_line]
    return lines

def make_coordinates(image, line_parameters):
    slope, intercept = line_parameters

    y1 = image.shape[0] # Height
    y2 = int(y1*(3/5)) # ??????
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)


    points = [x1, y1, x2, y2]
    return points



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



while(cap.isOpened()):
    ret, frame = cap.read()
    img = frame

    lane_image = np.copy(img) # Background lane image

    canny_image = canny(img)

    cropped_image = region_of_interest(canny_image)

    #left_cropped_image = cropped_image[:, :633, :]
    #right_cropped_image = cropped_image[:, 633:, :]

    lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)

    averaged_lines = average_slope_intercept(lane_image, lines)

    line_image = display_lines(lane_image, averaged_lines)

    combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)


    cv2.imshow('test', combo_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()


