"""Track colours on skittlebot. Show X and Y only"""
from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np
import time

def compute_contours(cns):
    """Centroid stuff"""
    # find the largest contour in the mask, then use
    # it to compute the minimum enclosing circle and
    # centroid
    c = max(cnts, key=cv2.contourArea)
    ((x, y), radius) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    return center, radius, (x, y)

# illumination can be a problem due to colour value
# hsv? yuv?- define range (try hsv later)

# Colour range - hsv. H110-130 blueish.
# sv - right the way up to allow for illumination

# Lego thing: [90   0 240] [120 255 255]
lh = 90
uh = 120
lv = 220
hv = 255 

camera = PiCamera()
camera.resolution = (320, 240)
# camera.shutter_speed = 20000
camera.vflip = True
stream = PiRGBArray(camera, size=(320, 240))

time.sleep(0.1)

for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
    frame = stream.array

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_range = np.array([lh, 0, lv], np.uint8)
    upper_range = np.array([uh, 255, hv], np.uint8)

    # Create a mask around that colour
    inrange = cv2.inRange(hsv, lower_range, upper_range)


    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(inrange, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # find contours in the mask and initialize the current
    # (x, y) center of the object
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    
    if len(cnts) >0:
        center, radius, (x, y) = compute_contours(cnts)
        if radius > 5:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)
            cv2.putText(frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            cv2.putText(frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            _, w, _ = frame.shape
            hw = w / 2
            if x > hw + 10:
                print("Driving right", x, y)
            elif x < hw - 10:
                print("Driving left", x, y)
            else:
                print("Ramming speed!!!", x, y)

    cv2.imshow("Ranged", inrange)
    cv2.imshow("Frame", frame)
    print lower_range, upper_range
    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == ord('a') and lh > 0:
        lh -= 5
    elif k == ord('s') and lh < 255:
        lh += 5
    elif k == ord('k') and uh > 0:
        uh -= 5
    elif k == ord('l') and uh < 255:
        uh += 5
    elif k == ord('n') and lv > 0:
        lv -= 5
    elif k == ord('m') and lv < 255:
        lv += 5
    elif k == ord('z') and hv > 0:
        hv -= 5
    elif k == ord('x') and hv > 255:
        hv += 5
    stream.truncate(0)

