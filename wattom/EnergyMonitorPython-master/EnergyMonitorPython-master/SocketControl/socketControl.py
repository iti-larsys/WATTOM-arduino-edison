from abc import ABC, abstractmethod


class SocketControl(ABC):
    """
    Abstract class with usual method to control the socket
    """
    def __init__(self, voltage):
        self.voltage = voltage

    @abstractmethod
    def change_relay(self, state):
        pass

    def set_voltage(self, voltage):
        pass

    @abstractmethod
    def calibrate(self):
        pass
