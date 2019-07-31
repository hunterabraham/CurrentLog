class Rigol:
    def __init__(self):
        self.channel = 0
        self.voltage = 0
        self.current = 0
        self.ocp = 0

    def set_channel(self, channel):
        self.channel = channel

    def set_voltage(self, voltage):
        self.voltage = voltage

    def set_current(self, current):
        self.current = current

    def set_ocp(self, ocp):
        self.ocp = ocp

    def get_channel(self):
        return self.channel

    def get_voltage(self):
        return self.voltage

    def get_current(self):
        return self.current

    def get_ocp(self):
        return self.ocp
