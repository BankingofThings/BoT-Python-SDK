from pybleno import *
from bot_python_sdk.bleno.device import DeviceCharacteristic

class BlenoService(BlenoPrimaryService):
    def __init__(self):
        BlenoPrimaryService.__init__(self, {
          'uuid': '729BE9C43C614EFB884FB310B6FFFFD1',
          'characteristics': [
            DeviceCharacteristic()
          ]})

