import platform
import subprocess
import sys

import falcon

from bot_python_sdk.action_resource import ActionsResource
from bot_python_sdk.action_service import ActionService
from bot_python_sdk.activation_resource import ActivationResource
from bot_python_sdk.base_resource import BaseResource
from bot_python_sdk.bluetooth_service import BluetoothService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_resource import PairingResource
from bot_python_sdk.qr_code_resource import QRCodeResource
from bot_python_sdk.store import Store
from bot_python_sdk.utils import Utils


class Finn:
    __instance__ = None

    @staticmethod
    def get_instance():
        return Finn.__instance__

    def __init__(self):
        Logger.info('Finn', '__init__')

        if Finn.__instance__ is None:
            Finn.__instance__ = self
        else:
            raise Exception("Should only be initialized once")

        self.__configuration_service = ConfigurationService()
        self.__configuration_store = ConfigurationStore()
        self.__configuration = self.__configuration_store.get()
        self.__action_service = ActionService()

        __store = Store()

        if not __store.has_configuration():
            Logger.info('Finn', '__init__' + str(sys.argv))
            if len(sys.argv) != 2:
                Logger.info('Finn', '__init__ 1')
                id = input('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
                Logger.info('Finn', '__init__' + ' id = ' + id)
            elif len(sys.argv[1]) != 36:
                id = Logger.info('Finn', '__init__ 2')
                Logger.info('Finn', '__init__' + ' id = ' + id)
                input('Please enter a valid productID')
            else:
                # argv is the console input
                self.__productID = sys.argv[1]

                self.__start_server()

    def __start_server(self):
        # Start application
        # 1. this file
        # 2. gunicorn starts file api.py
        # 3. api.py starts instance of Finn
        __ip_address = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]

        Logger.info('Server', "starting with configuration... IP" + __ip_address)

        if Utils.is_valid(__ip_address):
            Logger.info('Server', "Detected IP Address :" + __ip_address)
        else:
            __ip_address = '127.0.0.1'
            Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + __ip_address)

        Logger.info('Server', "Starting server at URL: http://" + __ip_address + ':3001/')

        # Executes api.py and indirectly finn.py
        proc = subprocess.run(['gunicorn', '-b', __ip_address + ':3001', 'bot_python_sdk.api:api'])

        Logger.info('Finn', '__start_server' + ' proc.returncode = ' + str(proc.returncode))

    @staticmethod
    def on_api_ready():
        Logger.info('Finn', 'on_api_ready static')
        Finn.get_instance().on_api_ready()


def on_api_ready(self):
    Logger.info('Finn', 'on_api_ready')
    device_status = self.__configuration.get_device_status()

    system_platform = platform.system()

    api = falcon.API()
    api.add_route('/', BaseResource())
    api.add_route('/actions', ActionsResource(self.__action_service, self.__configuration_store))
    api.add_route('/pairing', PairingResource(self.__configuration_store))
    api.add_route('/activate', ActivationResource())
    api.add_route('/qrcode', QRCodeResource())

    if device_status is DeviceStatus.ACTIVE:
        Logger.info('Finn', '__init__' + ' Device is already active, no need to further configure')
        Logger.info('Finn', '__init__' + ' Server is waiting for requests to serve...')
        Logger.info('Finn', '__init__' + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
    elif device_status is DeviceStatus.PAIRED:
        Logger.info('Finn', '__init__' + ' Device state is PAIRED, resuming the configuration')
        self.__configuration_service.activate()
    else:
        Logger.info('Finn', '__init__' + ' Device not paired yet. productID = ' + self.__configuration.maker_id + ', deviceID = ' + self.__configuration.device_id + ', publickKey = ' + self.__configuration.public_key)
        if system_platform != 'Darwin' and self.__configuration.is_bluetooth_enabled():
            # Handle BLE specific events and callbacks
            BluetoothService().initialize()

        self.__configuration_service.initialize_configuration(self.__productID)

        self.__configuration_service.pair()
