    
from pybleno import *
import array
import struct
import sys
import traceback
import socket
import json
from builtins import str
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_service import PairingService

bleno = Bleno()
Location = 'Bluetooth Service'

class ConfigureCharacteristic(Characteristic):
    
    def __init__(self):
        self.option = {'uuid' : '2901', 'value' : 'desc'}
        Characteristic.__init__(self, {
            'uuid': '32BEAA1BD20B47AC9385B243B8071DE4',
            'properties': ['read','write'],
            'descriptors': [
                    Descriptor(self.option)],
            'value': None
            
          })
        self.byteData = bytearray()
        
        
    def onWriteRequest(self, data, offset, withoutResponse, callback):  
         if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
         else:
            callback(Characteristic.RESULT_SUCCESS)
        
         if offset > len(data):
            callback(bleno.Characteristic.RESULT_INVALID_OFFSET)
            Logger.error('Error in Characteristic')
         else:
            callback(Characteristic.RESULT_SUCCESS, data[offset:]);        
            details = json.loads(data)
            
            if details['Skip'] == True:
                Logger.info(Location, 'Connected device skipped Wifi setup. ' +
                'Initializing pairing process...')
                PairingService().run()
            else:
                wifiDetails = ''
                
                if details['SSID'] != '':
                    wifiDetails = 'ctrl_interface=DIR=/var/run/wpa_supplicant' + \
                                  ' GROUP=netdev\r\n update_config=1\r\n country=GB \r\n'+ \
                                  'network={ \r\n        ssid="' + details['SSID'] + \
                                  '" \r\n' + \
                                  '        psk="' + details['PWD'] + \
                                  '" \r\n        ' + \
                                  'key_mgmt=WPA-PSK \r\n}'
                    
                Logger.info(Location, 'Wifi setup complete. Initializing pairing process...')
                PairingService().run()
                time.sleep(3)


                subprocess.run(['sudo echo \'' + wifiDetails + '\' > ./wpa_supplicant.conf'],shell=True)

                subprocess.run(["sudo", "cp", "./wpa_supplicant.conf", "/etc/wpa_supplicant/"])
               

                subprocess.run(["sudo", "rm", "./wpa_supplicant.conf"])
                subprocess.run(["sudo", "sleep", "1", "&&", "reboot"])

    
    
    
        
    def onReadRequest(self, offset, callback):
        if not offset:
            data = {'BoT': 'Configuration Done'}
            Logger.info(Location,'Connected device configuration complete. ' +
            'Start pairing process...')
            self.byteData.extend(map(ord, json.dumps(data)))
            PairingService().run()
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
            
        