from bot_python_sdk.logger import Logger
import bluetooth
from bluetooth.ble import DiscoveryService, BeaconService
import time
from bluetooth import *



LOCATION = 'Bluetooth Service'
RESOURCE = 'ble'
UUID = '729BE9C4-3C61-4EFB-884F-B310B6FFFFD1'
MAJOR = 1
MINOR = 1
TXPOWER = 1
INTERVAL = 200


class BluetoothService:
   
    def ble_advertising(self):
        
        try:
            service = BeaconService()
            Logger.info(LOCATION, 'Start advertising...')
            service.start_advertising(UUID,MAJOR,MINOR,TXPOWER,INTERVAL)
            time.sleep(15)
            service.stop_advertising()
            returnResponse = {"response" : "success"}
        except:
            Logger.error(LOCATION, 'Failed advertising_ble_test')
            advertising_response = {"message" : "failed"}
             raise exception
        return advertising_response
        
