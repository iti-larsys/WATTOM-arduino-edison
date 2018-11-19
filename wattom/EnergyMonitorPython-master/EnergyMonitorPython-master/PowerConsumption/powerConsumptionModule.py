from abc import abstractmethod

from PublishSubscriber.Publisher import Publisher


class PowerConsumption(Publisher):
    """
    Class that handles the generic computation of power
    """

    def __init__(self, socket_control):
        """
        Constructor
        :param socket_control: SocketControl object
        """
        self.socketControl = socket_control
        self.mainVoltage = self.socketControl.voltage

    def get_power(self, samples):
        """
        Calculates the power using the current samples measured
        :param samples:
        :return:
        """
        result = 0
        print("Going to calculate power")

        for sample in samples["samples"]:
            result += sample * sample
        # Calculates RMS current. 3300 = 3.3V/mV. 1650 is the max ADC count i can get with 3.3V
        amp_rms = self.calculate_rms(result, len(samples["samples"]))
        # print("Calculate power")
        # Calculates Power as an integer
        # TODO: How to pass main voltage
        power = (amp_rms * self.mainVoltage)
        # print(round(power))
        # Ignores some of the noise
        print("power " + str(power))
        print("RMS " + str(amp_rms))
        if amp_rms <= 0.10:
            power = 0
            amp_rms = 0

        # Stores the samples in the processed sample queue
        # self.processedSamplesQueueLock.acquire()
        # self.processedSamplesQueue.put({'power': power, 'current': amp_rms, 'timestamp': str(samples["timestamp"])})
        # print("These are the processed samples: "+str(self.processedSamplesQueue) +  "this is my size" + str(self.processedSamplesQueue.qsize()))
        print("power " + str(power))
        print("RMS " + str(amp_rms))
        self.notify({'power': power, 'current': amp_rms, 'timestamp': str(samples["timestamp"])})
        # self.dataProcessingSemaphore.release()
        # self.processedSamplesQueueLock.release()

    @abstractmethod
    def calculate_rms(self, result, length):
        """
        Method used to calculate RMS
        :param result: Sum of a sample values squared
        :param length: Length of samples
        :return:
        """
        pass
