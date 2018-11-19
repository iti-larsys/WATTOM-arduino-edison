import mraa
import netifaces as ni
import signal
import socket
import sys
import time
from flask import Flask, request
from flask_socketio import SocketIO, emit

from DataAcquisition.edisonRead import EdisonRead
from LEDFeedback.addressableLed import AddressableLedController
from PowerConsumption.edisonPowerConsumption import EdisonPowerConsumption
from SocketControl.edisonControl import EdisonControl
from mDNS.MdnsAdvertisment import MdnsAdvertisment

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = "gevent"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

ip = ni.ifaddresses('wlan0')[2][0]['addr']

mainVoltage = 230  # TODO Comes from a configuration file

socket_control = EdisonControl(mainVoltage)

mDNS = MdnsAdvertisment()
x = mraa.Gpio(20)


def signal_handler(signal, frame):
    """
    Invoked when Ctrl+C is pressed
    :param signal:
    :param frame:
    :return:
    """
    print('You pressed Ctrl+C!')
    x.isrExit()
    mDNS.stop_advertise()
    AddressableLedController().stop_movement()
    sys.exit(0)


def register_interrupt():
    """
    Register an Software interrupt to handle the Arduino Heartbeats
    :return:
    """
    x.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_RISING, interrupt_handler, x)


def background_thread():
    """
    Background thread that handle all the code that is not related with the communication with the broker
    Like receiveing the hearbeats, reading and calculating power, and sending it to server
    :return:
    """
    register_interrupt()
    signal.signal(signal.SIGINT, signal_handler)
    read_module = EdisonRead(socket_control)
    power_consumption_module = EdisonPowerConsumption(socket_control)
    url1 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/plugs_events"
    url2 = "http://common_room-35d864a6c6aedaf32848a1dc00e6c9d962478dc1f6a4925:938cf5ebbbb69ec1ca07098326528ffc9a89db31fdc65454@192.168.10.145:3000/api/json/continuous_measuring"
    # dataSenderModule = DataSender(url1, url2)
    # eventDetectorModule = EventDetection(dataSenderModule)
    led_control_module = AddressableLedController()
    power_consumption_module.add(led_control_module)
    # power_consumption_module.add(dataSenderModule)
    # power_consumption_module.add(eventDetectorModule)

    while 1:
        # pass
        socketio.sleep(0.5)  # This can't be removed, otherwise the heartbeats sending will fail
        # samples = read_module.addDAQSample()
        # power_consumption_module.getPower(samples)


def interrupt_handler(gpio):
    """
    Handles the Arduino Heartbeats and sends it to the broker
    :param gpio:
    :return:
    """
    timestamp = time.time()
    print("Vou enviar heartbeat")
    # socketio.sleep(1)
    socketio.emit("heartbeat", {"timestamp": timestamp, "hostname": socket.gethostname()})


@socketio.on('initConfig')
def receive_initial_configs(message):
    socket_control.initialize_relay(message["relayState"])
    AddressableLedController().initialize_leds(message["leds"], message["relayState"], message["personNear"],
                                               message["delay"])


@socketio.on('changeRelayState')
def change_relay_state(message):
    socket_control.change_relay(message["relayState"])
    AddressableLedController().change_relay_state(message["relayState"])


@socketio.on('changePersonNear')
def change_person_near(message):
    AddressableLedController().person_change(message["personNear"])


@socketio.on('changeDelay')
def change_delay(message):
    AddressableLedController().change_delay(message["delay"])


@socketio.on('changePosition')
def change_position(message):
    AddressableLedController().changeLed(message["position"])


@socketio.on('my_ping')
def ping_pong():
    emit('my_pong')


@socketio.on('selected')
def selected(message):
    AddressableLedController().make_selected_feedback(message["led"])


@socketio.on('stop')
def selected(message):
    AddressableLedController().stop_movement()


@socketio.on('connect')
def test_connect():
    print("Client connected")
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    mDNS.advertise()
    socketio.run(app, host=ip)
