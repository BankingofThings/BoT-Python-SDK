import json
import socket

from pybleno import *

from bot_python_sdk.data.storage import Storage
from bot_python_sdk.util.logger import Logger


# Device Characteristic
class DeviceCharacteristic(Characteristic):

    # On initializing this class the uuid and read property is defined
    def __init__(self):
        Logger.info('DeviceCharacteristic', '__init__')
        Characteristic.__init__(self, {
            'uuid': 'CAD1B5132DA446099908234C6D1B2A9C',
            'properties': ['read'],
        })
        # define/create a store for data bytes
        self.deviceData = bytearray()

    ###
    # OnReadRequest is triggered when device specific data are required. As per the offset
    # the data is prepared and sent back via the callback. On first request the offset
    # will be 0, hence the function compiles the device characteristics data and returns
    # it via the callback. Depending on the offset values, the data is returned through the
    # callback during subsequent calls to this API. The sent data is of JSON format.
    ##
    def onReadRequest(self, offset, callback):
        Logger.info('DeviceCharacteristic', 'onReadRequest' + str(offset))

        if not offset:
            configuration = Storage.get_configuration_object()
            Logger.info('DeviceCharacteristic', 'Device data being read by connected device.')
            device_information = configuration.get_device_information()

            data = {
                'deviceID': device_information['deviceID'],
                'productID': device_information['productID'],
                'name': socket.gethostname(),
                'publicKey': device_information['publicKey']
            }

            # Multipairing mode checks
            if configuration.get_is_multi_pair():
                data['multipair'] = 1
                data['aid'] = device_information['aid']

            self.deviceData.clear()
            self.deviceData.extend(map(ord, json.dumps(data)))
            Logger.info('DeviceCharacteristic', json.dumps(data))
        else:
            Logger.info('DeviceCharacteristic', 'onReadRequest 2 ' + str(offset))

        # Return through the callback the necessary data
        callback(Characteristic.RESULT_SUCCESS, self.deviceData[offset:])
