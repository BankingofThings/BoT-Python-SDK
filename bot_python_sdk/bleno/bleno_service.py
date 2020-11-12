from pybleno import *
from bot_python_sdk.bleno.device_characteristic import DeviceCharacteristic
from bot_python_sdk.bleno.device_info_characteristic import DeviceInfoCharacteristic
from bot_python_sdk.bleno.configure_characteristic import ConfigureCharacteristic
from bot_python_sdk.bleno.device_network_characteristic import DeviceNetworkCharacteristic
from bot_python_sdk.util.logger import Logger


class BlenoService(BlenoPrimaryService):

    # Bleno primary service, responsible for advertising frames.
    # Register the necessary characteristics
    def __init__(self, wifi_done_callback):
        Logger.info('BlenoService', '__init__')

        BlenoPrimaryService.__init__(self, {
            'uuid': '729BE9C43C614EFB884FB310B6FFFFD1',
            'characteristics': [
                DeviceCharacteristic(),
                DeviceInfoCharacteristic(),
                DeviceNetworkCharacteristic(),
                ConfigureCharacteristic(wifi_done_callback),
            ]})
