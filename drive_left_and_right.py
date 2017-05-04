import time
import gpiozero as gp

l = gp.Motor(6, 13)
r = gp.Motor(2, 3)
pan = gp.AngularServo(12)
tilt = gp.AngularServo(8)

time.sleep(10)

try:
  l.forward()
  r.forward()
  time.sleep(2)
  l.backward()
  time.sleep(0.5)
  l.forward()
  time.sleep(1)
  r.backward()
  time.sleep(0.5)
  r.forward()
  time.sleep(1)
finally:
  r.stop()
  l.stop()
  pan.angle =0
  pan.detach()
  tilt.angle =0
  tilt.detach()
