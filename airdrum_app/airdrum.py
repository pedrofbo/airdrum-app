from collections import deque
import time

import cv2
import imutils
import numpy as np

from drum import Drum
from utils import image_resize

cap = cv2.VideoCapture(0)
img_path = '../images/drum-v0.png'
drum_image = image_resize(cv2.imread(img_path), height=530)
drum_image = cv2.cvtColor(drum_image, cv2.COLOR_BGR2BGRA)

drum_red = Drum()
drum_blue = Drum()

# first color
red_lower = (0, 101, 161)
red_upper = (16, 236, 255)

# second color 
blue_lower = (167, 123, 99)
blue_upper = (180, 227, 193)

areas_red = deque(maxlen=24)
areas_blue = deque(maxlen=24)


def render_and_detect(frame, drum, lower_upper, areas, threshold=1.1):
    lower, upper = lower_upper
    hit = False
    if len(areas) == 24:
        if np.array(areas)[-4:].mean() > np.array(areas).mean() * threshold:
            print("hit")
            hit = True

    # red mask
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # for the red Object
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None
    # startpoint, endpoint, color, thickness
    if len(contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

        if hit is True:
            drum.hit((int(center[0]), int(center[1])))
        areas.append(cv2.contourArea(c))

    return areas

while True:
    
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, height=700, width=900)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    frame_h, frame_w, frame_c = frame.shape
    drum_h, drum_w, drum_c = drum_image.shape
    overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')

    offset = 20
    h_offset = frame_h - drum_h
    w_offset = frame_w - drum_w - offset

    overlay[h_offset:h_offset + drum_h, w_offset:w_offset + drum_w] = drum_image
    cv2.addWeighted(overlay, 0.6, frame, 1, 0, frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # image/frame, start_point, end_point, color, thickness
    # red
    cv2.circle(frame, (135, 465), 104, (0, 0, 255), 1)
    cv2.circle(frame, (233, 280), 102, (0, 0, 255), 1)
    cv2.circle(frame, (660, 280), 51, (0, 0, 255), 1)
    cv2.circle(frame, (775, 395), 104, (0, 0, 255), 1)

    # green
    cv2.circle(frame, (310, 550), 87, (0, 255, 0), 1)
    cv2.circle(frame, (650, 565), 106, (0, 255, 0), 1)

    # blue
    cv2.circle(frame, (395, 358), 73, (255, 0, 0), 1)
    cv2.circle(frame, (548, 358), 73, (255, 0, 0), 1)

    areas_red = render_and_detect(frame, drum_red, (red_lower, red_upper), areas_red)
    areas_blue = render_and_detect(frame, drum_blue, (blue_lower, blue_upper), areas_blue)

    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
