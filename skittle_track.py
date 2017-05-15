"""Track colours on skittlebot. Show X and Y only"""
from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction

from controlled_variable import ControlledVariable
import cv2
import numpy as np
import time

from skittlebot import Robot

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

def setup_camera():
    """SEt it up -warning - sleeps 2 seconds for camera to warm up"""
    camera = PiCamera()
    camera.resolution = (320, 240)
    time.sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = "off"
    gain = camera.awb_gains
    camera.awb_mode = "off"
    camera.awb_gains = gain
    camera.vflip = True
    return camera

# illumination can be a problem due to colour value

# Colour range - hsv. H110-130 blueish.
# sv - right the way up to allow for illumination

# Lego thing: [90   0 240] [120 255 255]
# Low light butterfly or skittle [90 10 240] [120 255 255]
# Green skittle - [ 35 130  80] [ 95 255 255], [30 80 85] [ 95 255 255]

# Hue
lh = ControlledVariable(0, 255, 90,  (ord('a'), ord('s')))
uh = ControlledVariable(0, 255, 120, (ord('k'), ord('l')))
# Saturation
ls = ControlledVariable(0, 255, 10,  (ord('q'), ord('w')))
hs = ControlledVariable(0, 255, 255, (ord('o'), ord('p')))
# Value
lv = ControlledVariable(0, 255, 240, (ord('z'), ord('x')))
hv = ControlledVariable(0, 255, 255, (ord('m'), ord('n')))

camera = setup_camera()
stream = PiRGBArray(camera, size=(320, 240))

use_motors = False

with Robot() as robot:
    time.sleep(0.1)
    robot.pan(90)
    robot.tilt(60)
    for frame in camera.capture_continuous(stream, format='bgr', use_video_port=True):
        frame = stream.array

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = np.array([lh.value, ls.value, lv.value], np.uint8)
        upper_range = np.array([uh.value, hs.value, hv.value], np.uint8)

        # Create a mask around that colour
        inrange = cv2.inRange(hsv, lower_range, upper_range)


        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(inrange, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # find contours in the mask and initialize the current
        # (x, y) center of the object
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        if len(cnts) > 0:
            center, radius, (x, y) = compute_contours(cnts)
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 3, (0, 0, 255), -1)
                cv2.putText(frame,"centroid", (center[0]+10,center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(frame,"("+str(center[0])+","+str(center[1])+")", (center[0]+10,center[1]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                cv2.putText(frame,"r"+str(int(radius)), (center[0]+10,center[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
                _, w, _ = frame.shape
                hw = 160
                if x < hw - 45:
                    print("Driving right", x, y)
                    if use_motors:
                        robot.right(90)
                        time.sleep(0.1)
                        robot.stop()
                elif x > hw + 45:
                    print("Driving left", x, y)
                    if use_motors:
                        robot.left(90)
                        time.sleep(0.1)
                        robot.stop()
                else:
                    print("Ramming speed!!!", x, y)
                    if use_motors:
                        robot.forward(60)
                        time.sleep(0.1)
                        robot.stop()
        else:
            if use_motors:
                robot.left(90)

        cv2.imshow("Ranged", inrange)
        cv2.imshow("Frame", frame)
        print lower_range, upper_range
        k = cv2.waitKey(1)
        if k == 27:
            break
        lh.handle_key(k)
        uh.handle_key(k)
        ls.handle_key(k)
        hs.handle_key(k)
        lv.handle_key(k)
        hv.handle_key(k)
        if k == ord('g'):
            use_motors = not use_motors
            if not use_motors:
                robot.stop()
        stream.truncate(0)

