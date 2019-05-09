    
from pybleno import *
import json
import subprocess
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_service import PairingService

bleno = Bleno()
LOCATION = 'Bluetooth Service'

# Cofiguration Characteristic
class ConfigureCharacteristic(Characteristic):
    # On initializing this class set the uuid for read and write request
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

    # Check the offset value to know the status of write request
    # Check the characteristic by using offset length
    # Start pairing service if device skipped wifi setup
    # Configure the wifi details with device and start the pairing service.
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        else:
            callback(Characteristic.RESULT_SUCCESS)
        
        if offset > len(data):
            callback(bleno.Characteristic.RESULT_INVALID_OFFSET)
            Logger.error(LOCATION, 'Error in Characteristic')
        else:
            callback(Characteristic.RESULT_SUCCESS, data[offset:]);        
            details = json.loads(data)
            
            if details['Skip'] == True:
                Logger.info(LOCATION, 'Connected device skipped Wifi setup. ' +
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
                    
                Logger.info(LOCATION, 'Wifi setup complete. Initializing pairing process...')
                PairingService().run()
                time.sleep(3)
                subprocess.run(['sudo echo \'' + wifiDetails + '\' > ./wpa_supplicant.conf'],shell=True)
                subprocess.run(["sudo", "cp", "./wpa_supplicant.conf", "/etc/wpa_supplicant/"])
                subprocess.run(["sudo", "rm", "./wpa_supplicant.conf"])
                subprocess.run(["sudo", "sleep", "1", "&&", "reboot"])
    
    # OnReadRequest shall be trigged when configure characteristics information
    # are needed. As per the offset the data shall be sent back via the callback.
    # On the first request the offset shall be 0, hence the function compiles
    # the necessary information w.r.t device configure information and returns through callback.
    # Since the entire data is not sent back by the caller, every time the offset value
    # is updated by the caller. This means from the specified offset the data needs to be sent
    # as byte sequence through CB. The sent data shall be of JSON format.
    def onReadRequest(self, offset, callback):
        if not offset:
            data = {'BoT': 'Configuration Done'}
            Logger.info(LOCATION,'Connected device configuration complete. ' +
            'Start pairing process...')
            self.byteData.extend(map(ord, json.dumps(data)))
            PairingService().run()
        callback(Characteristic.RESULT_SUCCESS, self.byteData[offset:])
            
