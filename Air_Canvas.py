import numpy as np
import cv2 as cv
from collections import deque

# Trackbar called Function
def func(x):
    pass

# Creating Trackbars for adjusting the marker color
cv.namedWindow("Color Detector")
cv.createTrackbar("Min Hue", "Color Detector", 33, 179, func)
cv.createTrackbar("Max Hue", "Color Detector", 153, 179, func)
cv.createTrackbar("Min Sat", "Color Detector", 72, 255, func)
cv.createTrackbar("Max Sat", "Color Detector", 255, 255, func)
cv.createTrackbar("Min Val", "Color Detector", 49, 255, func)
cv.createTrackbar("Max Val", "Color Detector", 255, 255, func)

# arrays to store colour points of different colours
blue = [deque(maxlen=1024)]
green = [deque(maxlen=1024)]
red = [deque(maxlen=1024)]
yellow = [deque(maxlen=1024)]

# indexes to mark points in particular array of particular colour

b_idx = 0
g_idx = 0
r_idx = 0
y_idx = 0

# Kernel for dilation
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] # [Blue, Green, Red, Yellow]
color_idx = 0

# Canvas Setup
AirCanvas = np.zeros((471,636, 3)) + 255
AirCanvas = cv.rectangle(AirCanvas, (40,1), (140,65), (0,0,0), 2)
AirCanvas = cv.rectangle(AirCanvas, (160,1), (255,65), colors[0], -1)
AirCanvas = cv.rectangle(AirCanvas, (275,1), (370,65), colors[1], -1)
AirCanvas = cv.rectangle(AirCanvas, (390,1), (485,65), colors[2], -1)
AirCanvas = cv.rectangle(AirCanvas, (505,1), (600,65), colors[3], -1)

cv.putText(AirCanvas, "CLEAR", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(AirCanvas, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(AirCanvas, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(AirCanvas, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(AirCanvas, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)
cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)

# Launching default webcam
frameWidth, frameHeight = 640, 480
capture = cv.VideoCapture(0)
capture.set(3, frameWidth) # setting the width of webcam (3 --> code for width)
capture.set(4, frameHeight) # setting the height of webcam (4 --> code for height)
capture.set(10, 150)  # setting the brightness of webcam (10 --> code for brightness)

while True:
    # Detecting frame from the camera
    isTrue, frame = capture.read()

    # Horizontally flipping the camera
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    min_hue = cv.getTrackbarPos("Min Hue", "Color Detector")
    max_hue = cv.getTrackbarPos("Max Hue", "Color Detector")
    min_sat = cv.getTrackbarPos("Min Sat", "Color Detector")
    max_sat = cv.getTrackbarPos("Max Sat", "Color Detector")
    min_val = cv.getTrackbarPos("Min Val", "Color Detector")
    max_val = cv.getTrackbarPos("Max Val", "Color Detector")

    upper_hsv = np.array([max_hue, max_sat, max_val])
    lower_hsv = np.array([min_hue, min_sat, min_val])

    # Adding buttons to the live frame for colour selection

    frame = cv.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv.putText(frame, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)

    # making mask of the pointer
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)
    mask = cv.erode(mask, kernel, iterations=1)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.dilate(mask, kernel, iterations=1)

    # Finding contours of the identified pointer
    cnts, _ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    center = None

    # If contours are formed
    if len(cnts) > 0:
        # sorting contours to find largest contour
        cnt = sorted(cnts, key=cv.contourArea, reverse=True)[0]

        # Get radius of the enclosing circle around the found contour
        ((x, y), radius) = cv.minEnclosingCircle(cnt)

        # Draw circle around the contour
        cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

        # Calculating center of detected contour
        mo = cv.moments(cnt)
        center = (int(mo['m10'] / mo['m00']), int(mo['m01'] / mo['m00']))

        # To check whether the user wants to click on any buttons

        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear button
                blue = [deque(maxlen=512)]
                green = [deque(maxlen=512)]
                red = [deque(maxlen=512)]
                yellow = [deque(maxlen=512)]

                b_idx = 0
                g_idx = 0
                r_idx = 0
                y_idx = 0

                AirCanvas[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                color_idx = 0 # Blue
            elif 275 <= center[0] <= 370:
                color_idx = 1 # Green
            elif 390 <= center[0] <= 485:
                color_idx = 2 # Red
            elif 505 <= center[0] <= 600:
                color_idx = 3 # Yellow
        else:
            if color_idx == 0:
                blue[b_idx].appendleft(center)
            elif color_idx == 1:
                green[g_idx].appendleft(center)
            elif color_idx == 2:
                red[r_idx].appendleft(center)
            elif color_idx == 3:
                yellow[y_idx].appendleft(center)
        # Append the next deque when nothing is detected to avoid messing up
    else:
        blue.append(deque(maxlen=512))
        b_idx += 1
        green.append(deque(maxlen=512))
        g_idx += 1
        red.append(deque(maxlen=512))
        r_idx += 1
        yellow.append(deque(maxlen=512))
        y_idx += 1
    # Draw lines of all the colors on the canvas and frame

    pts = [blue, green, red, yellow]
    for i in range(len(pts)):
        for j in range(len(pts[i])):
            for k in range(1, len(pts[i][j])):
                if pts[i][j][k - 1] is None or pts[i][j][k] is None:
                    continue
                cv.line(frame, pts[i][j][k - 1], pts[i][j][k], colors[i], 2)
                cv.line(AirCanvas, pts[i][j][k - 1], pts[i][j][k], colors[i], 2)

    # Show all windows
    cv.imshow("Camera", frame)
    cv.imshow("AirCanvas", AirCanvas)
    cv.imshow("mask", mask)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the Camera
capture.release()
cv.destroyAllWindows()
