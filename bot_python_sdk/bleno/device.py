    
from pybleno import *
import array
import struct
import sys
import traceback
import socket
import json
from builtins import str
from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration import Configuration
from bot_python_sdk.configuration_store import ConfigurationStore

bleno = Bleno()
Location = 'Bluetooth Service'

class DeviceCharacteristic(Characteristic):
    
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'CAD1B5132DA446099908234C6D1B2A9C',
            'properties': ['read'],
          })
        self.byteData = bytearray()
        self.configuration_store = ConfigurationStore() 
          
    def onReadRequest(self, offset, callback):
        
        if not offset:
            configuration = self.configuration_store.get()
            Logger.info(Location, 'Device data being read by connected device.')
            device_information = configuration.get_device_information()
           
            data = {
            'deviceID': device_information['deviceID'],
            'makerID': device_information['makerID'],
            'name': socket.gethostname(),
            'publicKey' : device_information['publicKey']
            }
          
           
            self.byteData.extend(map(ord, json.dumps(data)))
            
            
             
            Logger.info(Location, json.dumps(data))
            
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
