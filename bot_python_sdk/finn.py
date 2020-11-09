import subprocess

from bot_python_sdk.ActivationResource import ActivationResource
from bot_python_sdk.PairingResource import PairingResource
from bot_python_sdk.Utils import Utils
from bot_python_sdk.action_resource import ActionsResource
from bot_python_sdk.action_service import ActionService
from bot_python_sdk.base_resource import BaseResource
from bot_python_sdk.bluetooth_service import BluetoothService
from bot_python_sdk.configuration import Configuration
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.qr_code_resource import QRCodeResource
from bot_python_sdk.store import Store


class Finn:
    def __init__(self, product_id, device_status, aid, bluetooth_enabled, from_api):
        Logger.info('Finn', '__init__')

        self.__action_service = ActionService()

        # Server started, just continue with Finn.init
        if from_api:
            self.__configuration = Store.get_configuration_object()
            self.__init()
        # New install, no configuration, just create configuration and start server
        elif product_id is not None:
            public_key, private_key = KeyGenerator().generate_key()
            device_id = KeyGenerator().generate_uuid()
            # Added alternative id as an argument to initializing the configuration
            self.__configuration = Configuration()
            self.__configuration.initialize(product_id,
                                            device_id,
                                            device_status,
                                            bluetooth_enabled,
                                            aid,
                                            public_key,
                                            private_key)
            Store.save_configuration_object(self.__configuration)
            ConfigurationService.generate_qr_code()

            self.__start_server()
        # We have already configuration, just start server
        else:
            self.__start_server()

    def __init(self):
        import platform
        system_platform = platform.system()

        Logger.info('Finn', 'init' + ' system_platform = ' + system_platform)

        device_status = self.__configuration.device_status

        if device_status is DeviceStatus.ACTIVE:
            Logger.info('Finn', '__init__' + ' Device is already active, no need to further configure')
            Logger.info('Finn', '__init__' + ' Server is waiting for requests to serve...')
            Logger.info('Finn', '__init__' + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info('Finn', '__init__' + ' Device state is PAIRED, resuming the configuration')
            ConfigurationService.activate()
        else:
            Logger.info('Finn', '__init__' + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and self.__configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

                Logger.info('Finn', '__init__' + ' device_status.value = ' + device_status.value)

                ConfigurationService.pair()

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

    def init_api(self, api):
        Logger.info('Finn', 'init_api')

        api.add_route('/', BaseResource())
        api.add_route('/actions', ActionsResource(self.__action_service))
        api.add_route('/pairing', PairingResource())
        api.add_route('/activate', ActivationResource())
        api.add_route('/qrcode', QRCodeResource())
