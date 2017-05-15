from contextlib import contextmanager
import gpiozero as gp
import piconzero as pz

class _robot(object):
    def __init__(self):
        pz.init()
        self._pan = 0
        self._tilt = 1
        pz.setOutputConfig(self._pan, 2)
        pz.setOutputConfig(self._tilt, 2)
        self.tilt(90)
        self.pan(90)

    def tilt(self, angle):
        pz.setOutput(self._tilt, angle)

    def pan(self, angle):
        pz.setOutput(self._pan, angle)

    def forward(self, speed):
        """Both motors forward"""
        pz.forward(speed)

    def left(self, speed):
        pz.spinLeft(speed)

    def right(self, speed):
        pz.spinRight(speed)

    def backward(self, speed):
        pz.forward(-speed)

    def stop(self):
        """Both motors stop"""
        pz.stop()

@contextmanager
def Robot():
    """Use this to ensure robot stops if inner code 
        crashes"""
    try:
        yield _robot()
    finally:
        pz.stop()
        pz.cleanup()
