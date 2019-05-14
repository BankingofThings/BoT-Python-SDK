    
from pybleno import *
import netifaces
import json
from bot_python_sdk.logger import Logger

bleno = Bleno()

LOCATION = 'Bluetooth Service'
#Network Characteristics  class  provides network related data.
class DeviceNetworkCharacteristic(Characteristic):
    
    #On initialize this class the necessary UUID and the read property is to be set.
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'C42639DC270D4690A8B36BA661C6C899',
            'properties': ['read'],
          })
        self.byteData = bytearray()
          
    
    
    # OnReadRequest shall be trigged when device network characteristics information
    # are needed. As per the offset the data shall be sent back via the callback.
    # On the first request the offset shall be 0, hence the function compiles
    # the necessary information w.r.t network related information and returns through callback.
    # Since the entire data is not sent back by the caller, every time the offset value
    # is updated by the caller. This means from the specified offset the data needs to be sent
    # as byte sequence through CB. The sent data shall be of JSON format.
    def onReadRequest(self, offset, callback):
        if not offset:
            Logger.info(LOCATION, 'Device Network info being read by connected device.')
            interfaces = netifaces.interfaces()
            address = ''
            interface_name = ''        
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                # Skip local address
                if not iface.startswith('lo'):    
                    try:
                        # Filter only ipv4 address
                        ipv4Address = addrs[netifaces.AF_INET]
                        for ipv4 in ipv4Address:
                            address = ipv4['addr']
                            interface_name = iface        
                    except Exception as exception:
                        # Filter only ipv4 address
                        pass 
            data = {    
            'network': address,
            'ip': interface_name
            }
            self.byteData.extend(map(ord, json.dumps(data)))
        
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
            
