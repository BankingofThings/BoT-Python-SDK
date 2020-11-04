import sys

from bot_python_sdk.api import *
from bot_python_sdk.bluetooth_service import BluetoothService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


class Finn:
    def __init__(self, __api):
        Logger.info(Finn.__name__, Finn.__init__.__name__)

        __api.add_route(BASE_ENDPOINT, BaseResource())
        __api.add_route(ACTIONS_ENDPOINT, ActionsResource())
        __api.add_route(PAIRING_ENDPOINT, PairingResource())
        __api.add_route(ACTIVATION_ENDPOINT, ActivationResource())
        __api.add_route(QRCODE_ENDPOINT, QRCodeResource())

        self.__configuration_service = ConfigurationService()
        self.__configuration_store = ConfigurationStore()
        self.__configuration = self.__configuration_store.get()

        __store = Store()

        if not __store.has_configuration():
            if len(sys.argv) != 2:
                exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
            elif len(sys.argv[1]) != 36:
                exit('Please enter a valid productID')
            else:
                # argv is the console input
                __productID = sys.argv[1]

                Logger.info('Server', "starting with configuration. ProductID " + __productID)
                self.__configuration_service.initialize_configuration(__productID)

    def __on_server_start_done(self):
        Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__)

        configuration = ConfigurationStore().get()
        device_status = configuration.get_device_status()

        import platform
        system_platform = platform.system()

        Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' system_platform = ' + system_platform)

        if device_status is DeviceStatus.ACTIVE:
            Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' Device is already active, no need to further configure')
            Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' Server is waiting for requests to serve...')
            Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' Device state is PAIRED, resuming the configuration')
            self.__configuration_service.resume_configuration()
        else:
            Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

                device_status = self.__configuration.get_device_status()

                Logger.info(Finn.__name__, Finn.__on_server_start_done.__name__ + ' device_status.value = ' + device_status.value)

                if device_status == DeviceStatus.NEW:
                    self.__configuration_service.pair()
                if device_status == DeviceStatus.PAIRED:
                    self.__configuration_service.activate()
