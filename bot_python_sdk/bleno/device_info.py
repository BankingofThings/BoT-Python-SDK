from pybleno import *

import array
import struct
import sys
import traceback
import socket
import platform
import json
from builtins import str
import os
import json
from psutil import virtual_memory
from bot_python_sdk.logger import Logger

bleno = Bleno()

Location = 'Bluetooth Service'
class DeviceInfoCharacteristic(Characteristic):
    
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'CD1B3A04FA3341AAA25B8BEB2D3BEF4E',
            'properties': ['read']
          })
        self.byteData = bytearray()
        

          
          
    def onReadRequest(self, offset, callback):        
        if not offset:
            Logger.info(Location, 'Device Info being read by connected device.')
            total_memory = virtual_memory()
            data = {
            'platform':platform.system(),
            'release':platform.release(),
            'type': platform.uname().system,
            'arch': platform.uname().machine,
            'cpus': json.dumps(os.cpu_count()),
            'hostname': socket.gethostname(),
            'endianness': sys.byteorder,
            'totalMemory': total_memory.total
            }
            
            self.byteData.extend(map(ord, json.dumps(data)))
            
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:]);

           