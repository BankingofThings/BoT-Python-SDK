import sys

from bot_python_sdk.ActivationResource import ActivationResource
from bot_python_sdk.PairingResource import PairingResource
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
    def __init__(self, api):
        self.__configuration_service = ConfigurationService()
        self.__configuration_store = ConfigurationStore()
        self.__configuration = self.__configuration_store.get()
        __action_service = ActionService()

        Logger.info(Finn.__name__, Finn.__init__.__name__)

        api.add_route('/', BaseResource())
        api.add_route('/actions', ActionsResource(__action_service, self.__configuration_store))
        api.add_route('/pairing', PairingResource(self.__configuration_store))
        api.add_route('/activate', ActivationResource())
        api.add_route('/qrcode', QRCodeResource())

        __store = Store()

        if not __store.has_configuration():
            if len(sys.argv) != 2:
                exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
            elif len(sys.argv[1]) != 36:
                exit('Please enter a valid productID')
            else:
                # argv is the console input
                __productID = sys.argv[1]

                Logger.info(Finn.__name__, Finn.__init__.__name__ + "starting with configuration. ProductID " + __productID)
                self.__configuration_service.initialize_configuration(__productID)

        configuration = ConfigurationStore().get()
        device_status = configuration.get_device_status()

        import platform
        system_platform = platform.system()

        Logger.info(Finn.__name__, Finn.__init__.__name__ + ' system_platform = ' + system_platform)

        if device_status is DeviceStatus.ACTIVE:
            Logger.info(Finn.__name__, Finn.__init__.__name__ + ' Device is already active, no need to further configure')
            Logger.info(Finn.__name__, Finn.__init__.__name__ + ' Server is waiting for requests to serve...')
            Logger.info(Finn.__name__, Finn.__init__.__name__ + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info(Finn.__name__, Finn.__init__.__name__ + ' Device state is PAIRED, resuming the configuration')
            self.__configuration_service.resume_configuration()
        else:
            Logger.info(Finn.__name__, Finn.__init__.__name__ + ' Pair the device either using QRCode or Bluetooth Service through FINN Mobile App')
            if system_platform != 'Darwin' and configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

                device_status = self.__configuration.get_device_status()

                Logger.info(Finn.__name__, Finn.__init__.__name__ + ' device_status.value = ' + device_status.value)

                if device_status == DeviceStatus.NEW:
                    self.__configuration_service.pair()
                if device_status == DeviceStatus.PAIRED:
                    self.__configuration_service.activate()
