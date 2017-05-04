import time
import gpiozero as gp

pan = gp.AngularServo(12)
tilt = gp.AngularServo(8)
r = Robot(left=(6, 13), right=(2,3))
