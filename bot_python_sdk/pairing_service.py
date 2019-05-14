import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.logger import Logger
import json

LOCATION = 'Pairing Service'
RESOURCE = 'pair'
POLLING_INTERVAL_IN_SECONDS = 5
MAXIMUM_TRIES = 3


class PairingService:

    def __init__(self):
        configuration = ConfigurationStore().get()
        self.maker_id = configuration.get_maker_id()
        self.device_id = configuration.get_device_id()
        self.device_status = configuration.get_device_status()
        self.bot_service = BoTService()

    def run(self):
        
        # Multipairing device and new device can pair device.
        if not self.isPairable:
            return
        
        if(self.device_status ==  DeviceStatus.MULTIPAIR):
            Logger.info(LOCATION, 'Multipair mode, no need to poll or delete keys...')
            return   
           
              
        Logger.info(LOCATION, 'Starting to pair device...')
        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Pairing device, attempt: ' + str(tries))
            if self.pair():
                return True
            time.sleep(POLLING_INTERVAL_IN_SECONDS)
        return False
    
    
    
    # Checking the device status for pairable.
    # Only Multi pairing and new device can pair with the mobile.
    def isPairable(self):
        
        if(self.device_status ==  DeviceStatus.MULTIPAIR):
            return True
        
        return self.device_status == DeviceStatus.NEW
             



    def pair(self):
        try:
            response = self.bot_service.get(RESOURCE)
        except:
            Logger.error(LOCATION, 'Failed pairing attempt.')
            return False

        if response['status'] is True:
            Logger.success(LOCATION, 'Device successfully paired.')
            return True
        else:
            Logger.error(LOCATION, 'Failed pairing attempt.')
            return False

