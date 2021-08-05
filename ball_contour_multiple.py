#matlab code for reference
'''
#!/usr/bin/env python

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the yellow frisbee
# in the HSV color space, then initialize the
# list of tracked points
yellowLower = (20, 100, 100)
yellowUpper = (40, 255, 255)

# yellowLower = (0, 0, 150)
# yellowUpper = (0, 0, 255)


pts = deque(maxlen=args["buffer"])

# grabbing the reference to the webcam
cap = VideoStream(src=0).start()

# allowing the camera or video file to warm up
time.sleep(2.0)

while (True):
    # grabbing the current frame
    frame = cap.read()

    # handling the frame from VideoCapture
    frame = frame[1] if args.get("video", False) else frame

    # resizing and blurring the frame and converting it to HSV color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # constructing a mask for the yellow, then performing dilations and erosions to remove blobs left in the mask
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # finding contours in the mask and initialize the (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    center = None

    # only proceeding if at least one contour was found
    if len(cnts) > 0:
        # finding the largest contour in the mask, then using it to compute the minimum enclosing circle and centroid
        #print(cnts)
        cnts.sort()
        c = max(cnts, key=cv2.contourArea)
        c1 = cnts[-2]
        #print(c)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX

        # displaying text on the center marker
        cv2.putText(frame, '.', center, font, 1, (50, 50, 50), 2, cv2.LINE_AA)

        # print center

        # only proceed if the radius meets a minimum size, changed to 10 for far away cases
        if radius > 20:
            # drawing the circle and centroid on the frame
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 0, 0), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)

    # updating the points queue
    pts.appendleft(center)

    # showing the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''