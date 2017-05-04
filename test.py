import gpiozero as gp
from time import sleep

ml = gp.Motor(6, 12)
mr = gp.Motor(2, 3)
print("all off")
ml.stop()
mr.stop()
try:
    sleep(2)
    print("l fwd")
    ml.forward()
    sleep(2)
    print("l backward")
    ml.backward()
    sleep(2)
    ml.stop()
    print("r fwd")
    mr.forward()
    sleep(2)
    print("r backward")
    mr.backward()
    sleep(2)
finally:
    print("all off")
    mr.stop()
