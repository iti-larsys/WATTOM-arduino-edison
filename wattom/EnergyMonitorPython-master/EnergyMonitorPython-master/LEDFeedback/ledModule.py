import threading
import time

import mraa

from PublishSubscriber.Subscriber import Subscriber


class LedController(Subscriber):
    """
    Class that handles the normal RGB LEDs to Energy Feedback
    """
    def __init__(self, pin_red, pin_blue, pin_green):
        """
        Constructor
        :param pin_red: GPIO Pin Number of Red LED
        :param pin_blue: GPIO Pin Number of Blue LED
        :param pin_green: GPIO Pin Number of Green LED
        """
        self.power = 0
        self.pwm_red = mraa.Pwm(pin_red)
        self.pwm_green = mraa.Pwm(pin_green)
        self.pwm_blue = mraa.Pwm(pin_blue)
        # Enables the pin's
        self.pwm_red.enable(True)
        self.pwm_green.enable(True)
        self.pwm_blue.enable(True)
        # self.processedSamplesQueue = processedSamplesQueue
        # self.processedSamplesQueueLock = processedSamplesQueueLock
        # STATE CONSTANTS
        self.CONST_STATE_GREEN = "green"
        self.CONST_STATE_YELLOW = "yellow"
        self.CONST_STATE_RED = "red"
        # Leds State
        self.current_state = self.CONST_STATE_GREEN
        self.past_state = self.CONST_STATE_GREEN
        # The color min value
        self.CONST_GRADIENT = 0.10
        # Starts with the led in green
        self.pin_red = 0.0000
        self.pin_blue = 0.0000
        self.pin_green = 0.0000
        """self.led(self.pinGreen,self.pinRed)
        """  # Data that is receive by the thread
        self.power_buffer = []
        self.led_semaphore_controller = threading.Semaphore(
            value=0)  # This will controll the led reads on the list that has the current values

    def led(self, value_green, value_red):
        """
        Led color change
        :param value_green:
        :param value_red:
        :return:
        """
        self.pwm_green.write(value_green)
        self.pwm_red.write(value_red)

    def change_state(self):
        """
        Will make the current state var according with the power received.
        :return:
        """

        self.past_state = self.current_state
        if self.power >= 1000:
            self.current_state = self.CONST_STATE_RED
        elif 300 < self.power < 1000:
            self.current_state = self.CONST_STATE_YELLOW
        else:
            self.current_state = self.CONST_STATE_GREEN

    def color_change(self):
        """
        Change colors of LEDs according with the consumption state
        :return:
        """
        if self.current_state == self.CONST_STATE_RED:
            if self.past_state == self.CONST_STATE_RED:
                self.led(0.0000, 1.0000)
                self.pin_red = 1.0000
                self.pin_green = 0.0000
            elif self.past_state == self.CONST_STATE_YELLOW:
                while self.pin_green > 0.0000 and self.pin_red < 1.0000:
                    self.pin_green = self.pin_green + self.CONST_GRADIENT
                    self.led(self.pin_green, 1.0000)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_RED
            else:
                while self.pin_green > 0.0000 and self.pin_red < 1.0000:
                    self.pin_red = self.pin_red + self.CONST_GRADIENT
                    self.pin_green = self.pin_green - self.CONST_GRADIENT
                    self.led(self.pin_green, self.pin_red)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_RED

        if self.current_state == self.CONST_STATE_YELLOW:
            if self.past_state == self.CONST_STATE_YELLOW:
                self.led(1.0000, 1.0000)
                self.pin_red = 1.0000
                self.pin_green = 1.0000
            elif self.past_state == self.CONST_STATE_RED:
                while self.pin_green < 1.0000:
                    self.pin_green = self.pin_green + self.CONST_GRADIENT
                    self.led(self.pin_green, 1.0000)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_YELLOW
            else:
                while self.pin_red < 1.0000:
                    self.pin_red = self.pin_red + self.CONST_GRADIENT
                    self.led(1.0000, self.pin_red)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_YELLOW

        if self.current_state == self.CONST_STATE_GREEN:
            if self.past_state == self.CONST_STATE_GREEN:
                self.led(1.0000,
                         0.0000)  # TODO PROBABLY NEED TO TI CHANFE THE GREEN VALUE AN NOT CHANGE IT SO NEED TO READ FROM THE PIN
                self.pin_red = 0.0000
                self.pin_green = 1.0000
            elif self.past_state == self.CONST_STATE_RED:
                while self.pin_green < 1.0000 and self.pin_red > 0.0000:
                    self.pin_red = self.pin_red - self.CONST_GRADIENT
                    self.pin_green = self.pin_green + self.CONST_GRADIENT
                    self.led(self.pin_green, self.pin_red)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_GREEN
            else:
                while self.pin_green < 1.0000 and self.pin_red > 0.0000:
                    self.pin_red = self.pin_red - self.CONST_GRADIENT
                    self.led(1.0000, self.pin_red)
                    time.sleep(0.1)
                self.past_state = self.CONST_STATE_GREEN

    def update(self, data):
        # print("LED receive power")
        self.power_buffer.append(data['power'])
        self.led_semaphore_controller.release()
        # print("Subscriber LED " + ))
        # self.changeState(data['power'])
        # self.colorChange()


"""
if __name__ == "__main__":
    ledContoller = LedController(20,14,21)

    while True:
        power = 0
        while power <= 4400:
            if ledContoller.currentState == ledContoller.CONST_NO_STATE:
                ledContoller.greenLedTransition()
                ledContoller.currentState = ledContoller.CONST_STATE_GREEN
"""
