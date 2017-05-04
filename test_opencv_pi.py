# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.shutter_speed = 20000
camera.vflip = True
rawCapture = PiRGBArray(camera)
 
# allow the camera to warmup
time.sleep(1)
 
# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imwrite("test.png", image)
