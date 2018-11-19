import time

from DataAcquisition.readModule import ADataAcquisition


class EdisonRead(ADataAcquisition):
    """
    Extension of ADataAcquisition to handle the readings using Inter Edison
    """
    def __init__(self, socket_control):
        """
        Constructor
        :param socket_control:An object of SocketControl
        """
        super().__init__(socket_control)
        self.samples = []
        self.samplesNum = 500
        self.sampleTime = 0.1
        self.sampleInterval = self.sampleTime / self.samplesNum
        self.adcZero = self.socketControl.calibrate()

    def add_d_acq_sample(self):
        """
        Reads the value of current measured during one second by the ADC
        :return: A dictionary with all the the samples read and a timestamp of the last reading
        """
        print("Reading function")
        self.samples = []
        start_time = time.time()
        while time.time() - start_time < 1:
            # Centers read value at zero
            read_value = self.adc.adc_read() - self.adcZero
            self.samples.append(read_value)
        # print(str(self.samples))
        return {"samples": self.samples, "timestamp": time.time()}
