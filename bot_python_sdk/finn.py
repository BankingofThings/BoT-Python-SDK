import subprocess
import sys

import falcon

from bot_python_sdk.ActivationResource import ActivationResource
from bot_python_sdk.PairingResource import PairingResource
from bot_python_sdk.Utils import Utils
from bot_python_sdk.action_resource import ActionsResource
from bot_python_sdk.action_service import ActionService
from bot_python_sdk.base_resource import BaseResource
from bot_python_sdk.bluetooth_service import BluetoothService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.qr_code_resource import QRCodeResource
from bot_python_sdk.store import Store


class Finn:
    __instance__ = None

    @staticmethod
    def get_instance():
        return Finn.__instance__

    def __init__(self):
        Finn.__instance__ = self

        self.__configuration_service = ConfigurationService()
        self.__configuration_store = ConfigurationStore()
        self.__configuration = self.__configuration_store.get()
        self.__action_service = ActionService()

        Logger.info('Finn', '__init__')

        __store = Store()

        if not __store.has_configuration():
            if len(sys.argv) != 2:
                exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
            elif len(sys.argv[1]) != 36:
                exit('Please enter a valid productID')
            else:
                # argv is the console input
                __productID = sys.argv[1]

                Logger.info('Finn', '__init__' + "starting with configuration. ProductID " + __productID)
                self.__configuration_service.initialize_configuration(__productID)

        self.__start_server()

        device_status = self.__configuration.get_device_status()

        import platform
        system_platform = platform.system()

        Logger.info('Finn', '__init__' + ' system_platform = ' + system_platform)

        if device_status is DeviceStatus.ACTIVE:
            Logger.info('Finn', '__init__' + ' Device is already active, no need to further configure')
            Logger.info('Finn', '__init__' + ' Server is waiting for requests to serve...')
            Logger.info('Finn', '__init__' + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info('Finn', '__init__' + ' Device state is PAIRED, resuming the configuration')
            self.__configuration_service.activate()
        else:
            Logger.info('Finn', '__init__' + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and self.__configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

                Logger.info('Finn', '__init__' + ' device_status.value = ' + device_status.value)

                self.__configuration_service.pair()

    def __start_server(self):
        Logger.info('Finn', '__start_server')
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
        subprocess.run(['gunicorn', '-b', __ip_address + ':3001', 'bot_python_sdk.api:api'])

    def on_server_ready(self):
        Logger.info('Finn', 'on_server_ready')
        api = application = falcon.API()
        api.add_route('/', BaseResource())
        api.add_route('/actions', ActionsResource(self.__action_service, self.__configuration_store))
        api.add_route('/pairing', PairingResource(self.__configuration_store))
        api.add_route('/activate', ActivationResource())
        api.add_route('/qrcode', QRCodeResource())
