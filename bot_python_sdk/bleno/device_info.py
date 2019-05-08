from pybleno import *
import sys
import socket
import platform
import json
import os
from psutil import virtual_memory
from bot_python_sdk.logger import Logger

bleno = Bleno()
LOCATION = 'Bluetooth Service'

#Device information Characteristic
class DeviceInfoCharacteristic(Characteristic):
    
    #On initializing this class set the device information characteristics UUID and the read property
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'CD1B3A04FA3341AAA25B8BEB2D3BEF4E',
            'properties': ['read']
          })
        #Define the data store for the  device info characteristics
        self.byteData = bytearray()       
    
    
    # OnReadRequest shall be trigged when device info characteristics information
    # are needed. As per the offset the data shall be sent back via the callback.
    # On the first request the offset shall be 0, hence the function compiles
    # the necessary information w.r.t device information and returns through callback.
    # Since the entire data is not sent back by the caller, every time the offset value
    # is updated by the caller. This means from the specified offset the data needs to be sent
    # as byte sequence through CB. The sent data shall be of JSON format.
    def onReadRequest(self, offset, callback):        
        if not offset:
            Logger.info(LOCATION, 'Device Info being read by connected device.')
            total_memory = virtual_memory()
            endian = sys.byteorder
            
            data = {
            'platform':platform.system(),
            'release':platform.release(),
            'type': platform.uname().system,
            'arch': platform.uname().machine,
            'cpus': json.dumps(os.cpu_count()),
            'hostname': socket.gethostname(),
            'totalMemory': total_memory.total
            }
            # Mapping endian value to match with node sdk
            if endian == 'little':
                data['endianness'] = 'LE'
            else:
                data['endianness'] = 'BE'
            self.byteData.extend(map(ord, json.dumps(data)))
        
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
