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

    lowred = np.array([131, 90, 106])
    highred = np.array([255, 255, 255])

    lowblue = np.array([40, 150, 116])
    highblue = np.array([255, 255, 255])

    red_mask = cv2.inRange(hsv, lowred, highred)
    blue_mask = cv2.inRange(hsv, lowblue, highblue)

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

    # for the red Object
    contours, hierachy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    # startpoint, endpoint, color, thickness
    for cnt in contours:
        (center, radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)
        # print((center[0], center[1]))
        drum.hit((int(center[0]), int(center[1])))
        break

    # for the blue Object
    contours, hierachy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    # # startpoint, endpoint, color, thickness
    for cnt in contours:
        (center, radius) = cv2.minEnclosingCircle(cnt)
        cv2.circle(frame, (int(center[0]), int(center[1])), int(radius), (0, 255, 0), 2)
        # print((center[0], center[1]))
        drum.hit((int(center[0]), int(center[1])))
        break

    cv2.imshow("frame", frame)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", res)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
