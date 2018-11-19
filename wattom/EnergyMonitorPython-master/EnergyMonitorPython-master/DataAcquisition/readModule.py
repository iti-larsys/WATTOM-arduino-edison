import time
from abc import ABC, abstractmethod


class ADataAcquisition(ABC):
    """
    Abstract class to read ernergy currrent samples
    """
    result = 0
    readValue = 0
    countSamples = 0
    timestamp = time.time()

    def __init__(self, socket_control):
        """
        Constructor
        :param socket_control: An Object from SocketControl class
        """
        self.socketControl = socket_control
        self.adc = self.socketControl.adc

    @abstractmethod
    def add_d_acq_sample(self):
        """
        Method used to read current sample
        :return:
        """
        pass
