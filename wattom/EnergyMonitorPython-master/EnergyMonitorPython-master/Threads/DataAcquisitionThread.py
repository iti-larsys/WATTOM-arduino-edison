import threading
from DataAcquisition.edisonRead import EdisonRead
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption

class DataAcquisitionThread(threading.Thread):
    def __init__(self, socketControl, dataProcessingSemaphore, powerSamples):
        threading.Thread.__init__(self)
        self.readModule = EdisonRead(socketControl)
        self.powerConsumptionModule = EdisonPowerConsumption(socketControl, dataProcessingSemaphore, powerSamples)

    def run(self):
        while True:
            samples = self.readModule.addDAQSample()
            self.powerConsumptionModule.getPower(samples)
