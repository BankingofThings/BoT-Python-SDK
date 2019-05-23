from pybleno import *
from bot_python_sdk.bleno.device import DeviceCharacteristic
from bot_python_sdk.bleno.device_info import DeviceInfoCharacteristic
from bot_python_sdk.bleno.configure import ConfigureCharacteristic
from bot_python_sdk.bleno.device_network import DeviceNetworkCharacteristic

#Bleno primary service uuid
BLENO_PRIMARY_SERVICE_UUID = '729BE9C43C614EFB884FB310B6FFFFD1'

class BlenoService(BlenoPrimaryService):
    '''
    Bleno primary service, responsible for advertising frames.
    Register the necessay characteristics
    '''
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
            'uuid': BLENO_PRIMARY_SERVICE_UUID,
            'characteristics': [
                DeviceCharacteristic(),
                DeviceInfoCharacteristic(),
                DeviceNetworkCharacteristic(),
                ConfigureCharacteristic()
            ]})
