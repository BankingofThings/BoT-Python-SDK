from pybleno import *
from bot_python_sdk.bleno.device import DeviceCharacteristic
from bot_python_sdk.bleno.device_info import DeviceInfoCharacteristic
from bot_python_sdk.bleno.configure import ConfigureCharacteristic
from bot_python_sdk.bleno.device_network import DeviceNetworkCharacteristic


class BlenoService(BlenoPrimaryService):
    
    #Advertising uuid for the device
    #Triggering all the charecteristics one by on on read request 
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
          'uuid': '729BE9C43C614EFB884FB310B6FFFFD1',
          'characteristics': [
              DeviceCharacteristic(),
              DeviceInfoCharacteristic(),
              DeviceNetworkCharacteristic(),
              ConfigureCharacteristic()
          ]})
