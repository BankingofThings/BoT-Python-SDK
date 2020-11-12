from pybleno import *
import sys
import socket
import platform
import json
import os
from psutil import virtual_memory
from bot_python_sdk.util.logger import Logger


# Device specific information characteristic
class DeviceInfoCharacteristic(Characteristic):

    # On initializing this class set the device information characteristics UUID and the read property
    def __init__(self):
        Logger.info('DeviceInfoCharacteristic', '__init__')

        Characteristic.__init__(self, {
            'uuid': 'CD1B3A04FA3341AAA25B8BEB2D3BEF4E',
            'properties': ['read']
        })
        # Define the data store for the  device info characteristics
        self.deviceInfoData = bytearray()

    ###
    # OnReadRequest is trigged when device info data are required. As per the offset
    # the data is prepared and sent back via the callback. On first request the offset
    # will be 0, hence the function compiles the device infomation data and returns
    # it via the callback. Depending on the offset values, the data is returned through the
    # callback during subsequent calls to this API. The sent data is of JSON format.
    ##
    def onReadRequest(self, offset, callback):
        Logger.info('DeviceInfoCharacteristic', 'onReadRequest')

        if not offset:
            Logger.info('DeviceInfoCharacteristic', 'Device Info being read by connected device.')
            system_data = {
                'platform': platform.system(),
                'release': platform.release(),
                'type': platform.uname().system,
                'arch': platform.uname().machine,
                'cpus': json.dumps(os.cpu_count()),
                'hostname': socket.gethostname(),
                'totalMemory': virtual_memory().total,
                'endianness': 'LE' if sys.byteorder == 'little' else 'BE'
            }
            # Mapping endian value to match with node sdk
            self.deviceInfoData.extend(map(ord, json.dumps(system_data)))
        # Return the necessary data through the call back
        callback(Characteristic.RESULT_SUCCESS, self.deviceInfoData[offset:])
