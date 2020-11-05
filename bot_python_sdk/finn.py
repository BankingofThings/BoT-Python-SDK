import sys
import platform

from bot_python_sdk.activation_resource import ActivationResource
from bot_python_sdk.pairing_resource import PairingResource
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

        Logger.info('Finn', '__init__')

        api.add_route('/', BaseResource())
        api.add_route('/actions', ActionsResource(__action_service, self.__configuration_store))
        api.add_route('/pairing', PairingResource(self.__configuration_store))
        api.add_route('/activate', ActivationResource())
        api.add_route('/qrcode', QRCodeResource())

        __store = Store()

        if not __store.has_configuration():
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
                __productID = sys.argv[1]

                Logger.info('Finn', '__init__' + "starting with configuration. ProductID " + __productID)
                self.__configuration_service.initialize_configuration(__productID)

        device_status = self.__configuration.get_device_status()

        system_platform = platform.system()

        Logger.info('Finn', 'deviceStatus = ' + str(device_status) + ', system_platform = ' + system_platform)

        if device_status is DeviceStatus.ACTIVE:
            Logger.info('Finn', '__init__' + ' Device is already active, no need to further configure')
            Logger.info('Finn', '__init__' + ' Server is waiting for requests to serve...')
            Logger.info('Finn', '__init__' + ' Supported Endpoints: /qrcode    /actions    /pairing    /activate')
        elif device_status is DeviceStatus.PAIRED:
            Logger.info('Finn', '__init__' + ' Device state is PAIRED, resuming the configuration')
            self.__configuration_service.activate()
        else:
            Logger.info('Finn', '__init__' + ' Device not paired yet. productID = ' + self.__configuration.maker_id + ', deviceID = ' + self.__configuration.device_id)
            if system_platform != 'Darwin' and self.__configuration.is_bluetooth_enabled():
                # Handle BLE specific events and callbacks
                BluetoothService().initialize()

            self.__configuration_service.pair()
