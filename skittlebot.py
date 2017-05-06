from contextlib import contextmanager
import gpiozero as gp

class Robot(object):
    def __init__(self):
        self.lm = gp.Motor(6, 13)
        self.rm = gp.Motor(2, 3)
        # self.pan = gp.AngularServo(12)
        # self.tilt = gp.AngularServo(8)


    @contextmanager
    def safe(self):
        """Use this to ensure robot stops if inner code 
        crashes"""
        try:
            yield
        finally:
            self.stop()


    def forward(self, speed):
        """Both motors forward"""
        self.lm.forward()
        self.rm.forward()

    def spinLeft(self, speed):
        self.lm.stop()
        self.rm.forward()

    def spinRight(self, speed):
        self.lm.forward()
        self.rm.stop()

    def stop(self):
        """Both motors stop"""
        self.lm.stop()
        self.rm.stop()
