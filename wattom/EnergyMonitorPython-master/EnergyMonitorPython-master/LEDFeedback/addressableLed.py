from threading import Timer

import mraa
import struct

from PublishSubscriber.Subscriber import Subscriber


class AddressableLedController(Subscriber):
    """
    Class that handles the connection between Intel Edison and Arduino to control NeoPixel LEDs
    """
    __instance = None
    x = mraa.Gpio(20)
    selected = False

    def __new__(cls):
        """
        Create a Singleton
        :return:
        """
        if AddressableLedController.__instance is None:
            AddressableLedController.__instance = object.__new__(cls)
        AddressableLedController.i2c = mraa.I2c(6)
        AddressableLedController.i2c.address(8)
        return AddressableLedController.__instance

    def change_power(self, power):
        """
        Prepares and send power data to Arduino
        :param power: value of power
        :return:
        """
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(power) & 0xFFFFFFFF)
        data = bytearray([1, y1, y2, y3, y4])  # ,power])
        self.change_leds(data)

    def change_relay_state(self, relay_state):
        """
        Prepares and send relay state data to Arduino
        :param relay_state:
        :return:
        """
        data = bytearray([2, relay_state])
        self.change_leds(data)

    def person_change(self, person_state):
        """
        Prepares and send person state data to Arduino
        :param person_state:
        :return:
        """
        print("person " + str(person_state))
        data = bytearray([4, person_state])
        self.change_leds(data)

    def change_delay(self, delay):
        """
        Prepares and send delay data to Arduino
        :param delay:
        :return:
        """
        print("Delay " + str(delay))
        # Done once
        int_to_four_bytes = struct.Struct('<I').pack
        # Done many times (you need to mask here, because your number is >32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([3, y1, y2, y3, y4])
        self.change_leds(data)

    def initialize_leds(self, leds, relay_state, person_near, delay):
        """
        Prepares and sends data to initialize de LEDs
        :param leds: an array of all expected LEDs to turn on
        :param relay_state: the state of the relay
        :param person_near: the state of the person
        :param delay: the value of delay
        :return:
        """
        print(leds)
        int_to_four_bytes = struct.Struct('<I').pack
        # This converts the delay in an array of 4 bytes (32 bits)
        y1, y2, y3, y4 = int_to_four_bytes(int(delay) & 0xFFFFFFFF)
        data = bytearray([0, relay_state, person_near, len(leds), y1, y2, y3, y4])
        self.change_leds(data)
        for led in leds:
            data = bytearray([4])
            data.append(int(led["position"]))
            data.append(int(led["orientation"]))
            data.append(int(led["red"]))
            data.append(int(led["green"]))
            data.append(int(led["blue"]))
            self.change_leds(data)

    def change_leds(self, data):
        """
        Code that sends the received data to Arduino
        :param data: the data to be sent
        :return:
        """
        print(data)
        AddressableLedController.i2c.write(data)
        print("Enviei")

    def make_selected_feedback(self, selected_led):
        """
        Prepares and send data to Arduino when a led is selected
        :param selected_led: the position of the selected LED
        :return:
        """
        data = bytearray([6, int(selected_led)])
        self.change_leds(data)
        # self.selected = True
        # Schedules the end of the selected feedback for 5 seconds after
        r = Timer(5.0, self.stop_selected_feedback, [int(selected_led)])
        r.start()

    def stop_selected_feedback(self, selected_led):
        """
        Prepares and send data to Arduino to stop the selected feedback
        :param selected_led:
        :return:
        """
        data = bytearray([7, selected_led])
        self.change_leds(data)
        # self.selected = False

    def stop_movement(self):
        """
        Prepares and send data to Arduino to stop the leds movement
        :return:
        """
        data = bytearray([8])
        self.change_leds(data)

    def update(self, data):
        """
        Implementation of update from Subscriber to receive the updated power values
        :param data: the data received by the Publisher with power value
        :return:
        """
        if not self.selected:
            self.change_power(data["power"])
