import subprocess
import sys

from bot_python_sdk.Utils import Utils
from bot_python_sdk.bluetooth_service import BluetoothService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger


class Finn:
    def __init__(self):
        Logger.info(Finn.__name__, Finn.__init__.__name__)
        self.__configuration_service = ConfigurationService()

        store = Store()

        if not store.has_configuration():
            if len(sys.argv) != 2:
                exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
            elif len(sys.argv[1]) != 36:
                exit('Please enter a valid productID')
            else:
                # argv is the console input
                productID = sys.argv[1]

                Logger.info('Server', "starting with configuration. ProductID " + productID)
                self.__configuration_service.initialize_configuration(productID)

        self.__start_server()

    @staticmethod
    def on_server_start_done():
        Logger.info(Finn.__name__, Finn.on_server_start_done.__name__)

        configuration = ConfigurationStore().get()
        device_status = configuration.get_device_status()

        import platform
        system_platform = platform.system()

        Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' system_platform = ' + system_platform)

        if device_status is DeviceStatus.ACTIVE:
            Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' Device is already active, no need to further configure')
            Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' Server is waiting for requests to serve...')
            Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' Device state is PAIRED, resuming the configuration')
            ConfigurationService().resume_configuration()
        else:
            Logger.info(Finn.__name__, Finn.on_server_start_done.__name__ + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

                device_status = self.configuration.get_device_status()

                Logger.info(LOCATION, 'DeviceStatus = ' + device_status.value)

                if device_status == DeviceStatus.NEW:
                    self.pair()
                if device_status == DeviceStatus.PAIRED:
                    self.activate()

    def __start_server(self):
        ip_address = self.__get_ip()

        Logger.info('Server', "starting with configuration... IP" + ip_address)

        if Utils.is_valid(ip_address):
            Logger.info('Server', "Detected IP Address :" + ip_address)
        else:
            ip_address = '127.0.0.1'
            Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + ip_address)

        Logger.info('Server', "Starting server at URL: http://" + ip_address + ':3001/')
        subprocess.run(['gunicorn', '-b', ip_address + ':3001', 'bot_python_sdk.api:api'])
        Logger.info('Server', 'Server is running')

    def __get_ip(self):
        return subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]
