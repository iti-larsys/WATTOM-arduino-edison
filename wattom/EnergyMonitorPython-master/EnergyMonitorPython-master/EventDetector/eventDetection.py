import time

from PublishSubscriber.Subscriber import Subscriber


class EventDetection(Subscriber):
    """
    Class that handles all the code for rising events (on/off)
    """
    def __init__(self, data_sender):
        """
        Constructor
        :param data_sender: an object of DataSender
        """
        self.store_power_samples = []  # an array to store a window of 5 power samples used to detect events
        self.previous_event_time = 0
        self.timeThreshold = 5
        self.power_threshold = 25
        self.data_sender = data_sender

    def update(self, data):
        """
        Implementation of update from Subscriber class
        :param data: a dictionary with power data
        :return:
        """
        print("Going to check event")
        self.detect_event(data["power"])

    def detect_event(self, power):
        """
        Detects events
        :param power: last value of power measured
        :return:
        """
        state_value = ""
        print("Calculating event")
        self.store_power_samples.append(power)
        if len(self.store_power_samples) >= 5:
            # Calculates the average when the buffer is full
            store_average_power_begin = (self.store_power_samples[0] + self.store_power_samples[1]) / 2
            store_average_power_end = (self.store_power_samples[3] + self.store_power_samples[4]) / 2
            average_difference = store_average_power_begin - store_average_power_end  # Module difference between the averages
            if time.time() - self.previous_event_time >= self.timeThreshold:  # Block Event Detection
                if abs(average_difference) >= self.power_threshold:  # An event happened.
                    # Detects the triggers Up or Down
                    if average_difference < 0:
                        print(" ### Turned a new device on ###")
                        state_value = "ON"
                        self.previous_event_time = time.time()
                    elif average_difference >= 0:
                        print(" ### Turned a device off ###")
                        state_value = "OFF"
                        self.previous_event_time = time.time()
                    post_event_data = {'type': state_value, 'timestamp': time.time()}
                    self.data_sender.send_data_event(post_event_data)
            self.store_power_samples.pop(0)  # Remove one of the items it doesn't matter the order.
