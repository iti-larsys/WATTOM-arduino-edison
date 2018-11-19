import asyncio
import json
import threading

import aiohttp
import async_timeout

from PublishSubscriber.Subscriber import Subscriber


class DataSender(Subscriber):
    """
    Class that handles the coe used to send power data to the server
    """

    def __init__(self, collection_event_url, collection_data_url):
        """
        Constructor
        :param collection_event_url: API URL to send the data events to mongodb collection
        :param collection_data_url: API URL to send the power data to mongodb collection
        """
        self.EventCollectionUrl = collection_event_url
        self.DataCollectionUrl = collection_data_url
        self.buffer = []
        self.dataSendSemaphore = threading.Semaphore(value=0)

    def send_data_event(self, data):
        """
        Function made to send events data when they are detected.
        :param data: data to be sent
        :return:
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ask_to_send_event(loop, data))

    async def send_event(self, session, payload):
        """
        Prepares the sending of events data
        :param session: session data
        :param payload: data to be sent
        :return:
        """
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.EventCollectionUrl, headers=headers, data=json.dumps(payload)) as response:
                return

    async def ask_to_send_event(self, loop, data):
        """
        Tries to send events data
        :param loop: reference to the asyncio loop
        :param data: data to be sent
        :return:
        """
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.send_event(session, data)
        except:
            print("Error sending")

    async def send_data_values(self, session, payload):
        """
        Function made to send measured current and power values.
        :param session: session data
        :param payload: data to be sent
        :return:
        """
        with async_timeout.timeout(10):
            headers = {'content-type': 'application/json'}
            async with session.post(self.DataCollectionUrl, headers=headers, data=json.dumps(payload)) as response:
                return

    def request_exception(self, request, exception):
        """
        Informs when it's not possible to send data
        :param request: the request data
        :param exception: The exception thrown
        :return:
        """
        print("Unable to send data: " + str(exception))

    async def send_values(self, loop, data):
        """
        Tries to send power data to the server
        :param loop: reference to asyncio loop
        :param data: data to be sent
        :return:
        """
        try:
            async with aiohttp.ClientSession(loop=loop) as session:
                await self.send_data_values(session, data)
        except:
            print("Error sending")

    def update(self, data):
        """
        Receives power values and send them to the server
        :param data: power values
        :return:
        """
        print("Going to send power data")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_values(loop, data))
        # print("Going to send power data")
        # self.buffer.append(data)
        # self.dataSendSemaphore.release()


"""
if __name__ == "__main__":
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.77:3000/api/json/continuous_measuring"
    object = dataSender(url1, url2)

    while True:
        print("Sending Data Events")
        object.sendDataEvent({'type': "on", 'timestamp': str(time.time())})
        #object.sendDataValues({'power':'1024', 'current':'10', 'timestamp': str(time.time())})
"""
