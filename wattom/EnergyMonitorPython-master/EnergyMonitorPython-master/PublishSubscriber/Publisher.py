from abc import ABC


class Publisher(ABC):
    """
    Abstract Class Publisher implementing the Observer Pattern
    """
    subscribers = []

    def add(self, subscriber):
        """
        Adds a subscriber to a list of subscribers
        :param subscriber: the object to be subscribed
        :return:
        """
        self.subscribers.append(subscriber)

    def notify(self, data):
        """
        Notifies all subscribers that a change has happened
        :param: data to be sent to subscribers
        :return:
        """
        for subscriber in self.subscribers:
            subscriber.update(data)

            # Don't need to implement this thing
            # def remove(self):
            #    pass
