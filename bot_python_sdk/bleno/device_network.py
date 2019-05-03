    
from pybleno import *
import array
import struct
import sys
import traceback
import netifaces
import json
from builtins import str
from bot_python_sdk.logger import Logger
from bot_python_sdk.configuration import Configuration

bleno = Bleno()

Location = 'Bluetooth Service'
class DeviceNetworkCharacteristic(Characteristic):
    
    def __init__(self):
        Characteristic.__init__(self, {
            'uuid': 'C42639DC270D4690A8B36BA661C6C899',
            'properties': ['read'],
          })
        #self.value = buffer()
        self.byteData = bytearray()
          
          
    def onReadRequest(self, offset, callback):
        
        
        if not offset:
            Logger.info(Location, 'Device Network info being read by connected device.')
            interfaces = netifaces.interfaces()
        
            for iface in interfaces:
                addrs = netifaces.ifaddresses(iface)
                #Skip local address
                if not iface.startswith('lo'):
                    
                    try:
                        #filter only ipv4 address
                        ipv4Address = addrs[netifaces.AF_INET]
                        for ipv4 in ipv4Address:
                            address = ipv4['addr']
                            interface_name = iface
                            
                            
                    except Exception as exception:
                        #filter only ipv4 address
                        pass 
            
            data = {
                
            'network': address,
            'ip': interface_name
            }
            
            self.byteData.extend(map(ord, json.dumps(data)))
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:]);
            
