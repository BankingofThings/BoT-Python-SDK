import json
import subprocess
import time

from pybleno import *

from bot_python_sdk.util.logger import Logger


# Configuration Characteristic
class ConfigureCharacteristic(Characteristic):

    # On initializing this class set the uuid for read and write request
    def __init__(self, wifi_done_callback):
        Logger.info('ConfigureCharacteristic', '__init__')

        self.__wifi_done_callback = wifi_done_callback
        self.option = {'uuid': '2901', 'value': 'desc'}
        Characteristic.__init__(self, {
            'uuid': '32BEAA1BD20B47AC9385B243B8071DE4',
            'properties': ['read', 'write'],
            'descriptors': [Descriptor(self.option)],
            'value': None
        })
        self.configureData = bytearray()

    ###
    # onWriteRequest is called when a client wants to configure/update the Wifi Settings.
    # Once the configuration is done, the device is reboot automatically
    ##
    def onWriteRequest(self, data, offset, without_response, callback):
        Logger.info('ConfigureCharacteristic', 'onWriteRequest')

        if offset:
            callback(Characteristic.RESULT_ATTR_NOT_LONG)
        else:
            callback(Characteristic.RESULT_SUCCESS)
        if offset > len(data):
            callback(Characteristic.RESULT_INVALID_OFFSET)
            Logger.error('ConfigureCharacteristic', 'Error in Characteristic')
        else:
            callback(Characteristic.RESULT_SUCCESS)
            # decode the byte sequence sent from the client and prepare a JSON structure
            details = json.loads(data.decode())
            # skip wifi configuration
            skip_wifi_config = False
            try:
                skip_wifi_config = details['Skip']
            except:
                Logger.info('ConfigureCharacteristic', 'Wifi Configuration is available ..')
                # wifi configuration is enabled from the client
            if skip_wifi_config == True:
                Logger.info('ConfigureCharacteristic', 'Connected device skipped Wifi setup. ' +
                            'Initializing pairing process...')
                self.__wifi_done_callback()
            else:
                # if valid SSID provided then create the wpa supplicant configuration.
                wifi_details = ''
                if details['SSID'] != '':
                    wifi_details = 'ctrl_interface=DIR=/var/run/wpa_supplicant' + \
                                   ' GROUP=netdev\r\n update_config=1\r\n country=GB \r\n' + \
                                   'network={ \r\n        ssid="' + details['SSID'] + \
                                   '" \r\n' + \
                                   '        psk="' + details['PWD'] + \
                                   '" \r\n        ' + \
                                   'key_mgmt=WPA-PSK \r\n}'
                Logger.info('ConfigureCharacteristic', 'Wifi setup complete. Initializing pairing process...')
                self.__wifi_done_callback()
                time.sleep(3)
                subprocess.run(['sudo echo \'' + wifi_details + '\' > ./wpa_supplicant.conf'], shell=True)
                subprocess.run(["sudo", "cp", "./wpa_supplicant.conf", "/etc/wpa_supplicant/"])
                Logger.info('ConfigureCharacteristic', 'Wifi configuration done! Device reboot in progress')
                # run the necessary command to update the wpa supplicant file with in /etc/
                subprocess.run(["sudo", "rm", "./wpa_supplicant.conf"])
                subprocess.run(["sudo", "sleep", "1"])
                # reboot the device after successful update of wpa suppicant configuration
                subprocess.run(["sudo", "reboot"])

    ###
    # OnReadRequest is trigged when device configuration specific information is required. As per
    # the offset the data is prepared and sent back via the callback. On first request the offset
    # will be 0, hence the function compiles the device configuration related information and returns
    # it via the callback. On subsequent calls to this API, the data is returned (via the callback)
    # form the offset value sent through the API. The sent data is of JSON format.
    ##
    def onReadRequest(self, offset, callback):
        if not offset:
            Logger.info('ConfigureCharacteristic', 'Connected device configuration complete. Start pairing process...')

            data = {'BoT': 'Configuration Done'}
            self.configureData.clear()
            self.configureData.extend(map(ord, json.dumps(data)))
            self.__wifi_done_callback()
        callback(Characteristic.RESULT_SUCCESS, self.configureData[offset:])
