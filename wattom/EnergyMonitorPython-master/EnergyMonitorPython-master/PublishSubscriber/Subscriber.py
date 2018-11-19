from abc import ABC, abstractmethod


class Subscriber(ABC):
    """
    Abstract Class Publisher implementing the Observer Pattern
    """

    @abstractmethod
    def update(self, data):
        """
        What a subscriber after the publisher receive a value
        :param data: The data received from the publisher
        :return:
        """
        pass
