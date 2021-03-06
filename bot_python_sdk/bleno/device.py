from pybleno import *
import socket
import json
from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus

LOCATION = 'Bluetooth Service'
#Device characteristics uuid
BLENO_DEVICE_CHARACTERISTICS_UUID = 'CAD1B5132DA446099908234C6D1B2A9C'
#bleno object creation
bleno = Bleno()

#Device Characteristic
class DeviceCharacteristic(Characteristic):

    #On initializing this class the uuid and read property is defined
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': BLENO_DEVICE_CHARACTERISTICS_UUID,
            'properties': ['read'],
        })
        # define/create a store for data bytes
        self.deviceData = bytearray()
        self.configuration_store = ConfigurationStore() 
    
    '''
    OnReadRequest is trigged when device specific data are required. As per the offset
    the data is prepared and sent back via the callback. On first request the offset 
    will be 0, hence the function compiles the device characteristics data and returns 
    it via the callback. Depending on the offset values, the data is returned through the 
    callback during subsequent calls to this API. The sent data is of JSON format.  
    '''
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
            # Multipairing mode checks
            if(device_status == DeviceStatus.MULTIPAIR):
                data['multipair'] = 1
                data['aid'] = device_information['aid']        
            self.deviceData.extend(map(ord, json.dumps(data)))
            Logger.info(LOCATION, json.dumps(data))
        #Return through the callback the necessary data
        callback(Characteristic.RESULT_SUCCESS, self.deviceData[offset:])
