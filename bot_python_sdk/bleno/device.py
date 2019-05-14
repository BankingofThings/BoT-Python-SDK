from pybleno import *
import socket
import json
from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus

bleno = Bleno()
LOCATION = 'Bluetooth Service'

#Device Characteristic
class DeviceCharacteristic(Characteristic):
    
    #On initializing this class the uuid and read property is defined
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'CAD1B5132DA446099908234C6D1B2A9C',
            'properties': ['read'],
          })
        # define/create a store for data bytes
        self.byteData = bytearray()
        self.configuration_store = ConfigurationStore() 
    
    # OnReadRequest shall be trigged when device characteristics information
    # are needed. As per the offset the data shall be sent back via the callback.
    # On the first request the offset shall be 0, hence the function compiles
    # the necessary information w.r.t device characteristics and returns through callback.
    # Since the entire data is not sent back by the caller, every time the offset value
    # is updated by the caller. This means from the specified offset the data needs to be sent
    # as byte sequence through CB. The sent data shall be of JSON format.  
    def onReadRequest(self, offset, callback):        
        if not offset:
            configuration = self.configuration_store.get()
            Logger.info(LOCATION, 'Device data being read by connected device.')
            device_status = configuration.get_device_status()
            device_information = configuration.get_device_information()
            data = {
            'deviceID': device_information['deviceID'],
            'makerID': device_information['makerID'],
            'name': socket.gethostname(),
            'publicKey' : device_information['publicKey']
            }
            
                        
            # Added required information for Multipairing device.
            if(device_status == DeviceStatus.MULTIPAIR):
                data['multipair'] = 1
                data['aid'] = device_information['aid']
            
            self.byteData.extend(map(ord, json.dumps(data))) 
            Logger.info(LOCATION, json.dumps(data))
         
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
