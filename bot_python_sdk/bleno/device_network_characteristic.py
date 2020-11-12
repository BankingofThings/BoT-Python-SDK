from pybleno import *
import netifaces
import json
from bot_python_sdk.util.logger import Logger


# Network Characteristics  class  provides network related data.
class DeviceNetworkCharacteristic(Characteristic):

    # On initialize this class the necessary UUID and the read property is to be set.
    def __init__(self):
        Logger.info('DeviceNetworkCharacteristic', '__init__')

        Characteristic.__init__(self, {
            'uuid': 'C42639DC270D4690A8B36BA661C6C899',
            'properties': ['read'],
        })
        self.networkData = bytearray()

    ###
    # OnReadRequest is trigged when device network information are required. As per the offset
    # the data is prepared and sent back via the callback. On first request the offset  will be 0,
    # hence the function compiles the network related information and returns it via the callback.
    # On subsequent calls to this API, the data is returned (via the callback) form the offset
    # value sent through the API. The sent data is of JSON format.
    ##
    def onReadRequest(self, offset, callback):
        Logger.info('DeviceNetworkCharacteristic', 'onReadRequest')

        if not offset:
            Logger.info('DeviceNetworkCharacteristic', 'Device Network info being read by connected device.')
            interfaces = netifaces.interfaces()
            address = ''
            interface_name = ''
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                # Skip local address
                if not iface.startswith('lo'):
                    try:
                        # Filter only ipv4 address
                        ipv4_address_list = addrs[netifaces.AF_INET]
                        for ipv4 in ipv4_address_list:
                            address = ipv4['addr']
                            interface_name = iface
                    except Exception as exception:
                        # Filter only ipv4 address
                        pass
            data = {
                'network': address,
                'ip': interface_name
            }
            self.networkData.extend(map(ord, json.dumps(data)))
        # Return the necessary network related data through the callback
        callback(Characteristic.RESULT_SUCCESS, self.networkData[offset:])
