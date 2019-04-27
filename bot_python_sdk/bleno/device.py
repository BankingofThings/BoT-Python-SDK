   
from pybleno import *
import array
import struct
import sys
import traceback
import socket
from builtins import str
from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration import Configuration

bleno = Bleno()

class DeviceCharacteristic(Characteristic):
    
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'CAD1B5132DA446099908234C6D1B2A9C',
            'properties': ['read'],
          })
          
          
    def onReadRequest(self, offset, callback):
        self.configuration = Configuration()
        
        if not offset:
            data = {
            'deviceID': self.configuration.get_device_id(),
            'makerID': self.configuration.get_maker_id(),
            'name': socket.gethostname(),
            'publicKey' : self.configuration.get_public_key()
            }
            writeUInt8(data, 0)
            callback(Characteristic.RESULT_SUCCESS, data);
        else:
            callback(Characteristic.RESULT_ATTR_NOT_LONG, None)
        
            
