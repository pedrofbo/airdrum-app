from collections import deque
import time

from joblib import Parallel, delayed
import cv2
import imutils
import numpy as np

from drum import Drum
from utils import image_resize

cap = cv2.VideoCapture(0)
img_path = '../images/drum-v0.png'
drum_image = image_resize(cv2.imread(img_path), height=530)
drum_image = cv2.cvtColor(drum_image, cv2.COLOR_BGR2BGRA)
drum = Drum()

# first color
red_lower = (0, 101, 161)
red_upper = (16, 236, 255)

# second color 
blue_lower = (167, 123, 99)
blue_upper = (180, 227, 193)

last = time.time()
now = time.time()
times = []

areas = deque(maxlen=24)
hit = False

while True:
    last = now
    now = time.time()
    times.append(now - last)
    # print(np.array(times).mean())

    if len(areas) == 24:
        if np.array(areas)[-4:].mean() > np.array(areas).mean() * 1.3:
            print("hit")
            hit = True
        else:
            hit = False
    
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

    # red mask
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    red_mask = cv2.erode(red_mask, None, iterations=2)
    red_mask = cv2.dilate(red_mask, None, iterations=2)

    # for the red Object
    red_contours = cv2.findContours(red_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours = imutils.grab_contours(red_contours)
    red_center = None
    # startpoint, endpoint, color, thickness
    if len(red_contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(red_contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        red_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, red_center, 5, (0, 0, 255), -1)

        if hit is True:
            drum.hit((int(red_center[0]), int(red_center[1])))
        areas.append(cv2.contourArea(c))

    # blue mask
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    blue_mask = cv2.erode(blue_mask, None, iterations=2)
    blue_mask = cv2.dilate(blue_mask, None, iterations=2)

    # for the blue Object
    blue_contours = cv2.findContours(blue_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_contours = imutils.grab_contours(blue_contours)
    blue_center = None
    # startpoint, endpoint, color, thickness
    if len(blue_contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(blue_contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        blue_center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, blue_center, 5, (0, 0, 255), -1)

        drum.hit((int(blue_center[0]), int(blue_center[1])))

    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
