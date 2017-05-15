class ControlledVariable(object):
    """Variable controlled by keyboard signals"""
    def __init__(self, minimum, maximum, start, keys):
        self.minimum = minimum
        self.maximum = maximum
        self.current = start
        self.dec_key, self.inc_key  = keys

    @property
    def value(self):
        return self.current

    def handle_key(self, key):
        """Handle a key press and make the change"""
        if key == self.inc_key and self.current < self.maximum:
            self.current += 5
        elif key == self.dec_key and self.current > self.minimum:
            self.current -= 5
