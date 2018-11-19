import math
from PowerConsumption.powerConsumptionModule import PowerConsumption


class EdisonPowerConsumption(PowerConsumption):
    """
    Class that handles the computation of power using Intel Edison ADC
    """

    def __init__(self, socket_control):
        self.sensibility = 122.1  # (185 mV/A * 3,3 V)/5V = 122.1; 185 mV/A is the sensibility written on the datasheet of the sensor used
        super().__init__(socket_control)

    def calculate_rms(self, result, length):
        """
        Calculate the RMS adapted to the ADC and Current Sensor Used
        :param result:
        :param length:
        :return:
        """
        return (math.sqrt(result / length)) * 3300 / (self.sensibility * 1650)
