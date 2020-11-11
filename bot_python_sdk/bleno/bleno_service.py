from pybleno import *
from bot_python_sdk.bleno.device import DeviceCharacteristic
from bot_python_sdk.bleno.device_info import DeviceInfoCharacteristic
from bot_python_sdk.bleno.configure import ConfigureCharacteristic
from bot_python_sdk.bleno.device_network import DeviceNetworkCharacteristic
from bot_python_sdk.util.logger import Logger

# Bleno primary service uuid
BLENO_PRIMARY_SERVICE_UUID = '729BE9C43C614EFB884FB310B6FFFFD1'


class BlenoService(BlenoPrimaryService):

    # Bleno primary service, responsible for advertising frames.
    # Register the necessary characteristics
    def __init__(self, wifi_done_callback):
        Logger.info('BlenoService', '__init__')

        BlenoPrimaryService.__init__(self, {
            'uuid': BLENO_PRIMARY_SERVICE_UUID,
            'characteristics': [
                DeviceCharacteristic(),
                DeviceInfoCharacteristic(),
                DeviceNetworkCharacteristic(),
                ConfigureCharacteristic(wifi_done_callback),
            ]})
