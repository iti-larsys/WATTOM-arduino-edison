import logging
import socket
import sys

from zeroconf import ServiceInfo, Zeroconf

import netifaces as ni

ip = ni.ifaddresses('wlan0')[2][0]['addr']


class MdnsAdvertisment:
    """
    Class to make mDNS Advertisements of the socket
    """
    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.",
                       socket.gethostname() + "._http._tcp.local.",
                       socket.inet_aton(ip), 5000, 0, 0,
                       desc, socket.gethostname() + ".local.")

    def __init__(self):
        """
        Constructor
        """
        self.zeroconf = Zeroconf()

    def advertise(self):
        """
        Starts mDNS advertising
        :return:
        """
        logging.basicConfig(level=logging.DEBUG)
        if len(sys.argv) > 1:
            assert sys.argv[1:] == ['--debug']
            logging.getLogger('zeroconf').setLevel(logging.DEBUG)

        print("Registration of a service, press Ctrl-C to exit...")
        self.zeroconf.register_service(self.info)

    def stop_advertise(self):
        """
        Stops mDNS advertising
        :return:
        """
        print("Unregistering...")
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
