from pybleno import *

import sys

import signal
import platform
import socket
from bot_python_sdk.logger import Logger
from bot_python_sdk.bleno.bleno_service import BlenoService


LOCATION = 'Bluetooth Service'
blenoService = BlenoService()
bleno = Bleno() 
class BluetoothService:
    
    def initialize(self):
        active =True
        bleno.on('stateChange',self.onStateChange)
        bleno.on('advertisingStart', self.onAdvertisingStart)
        bleno.start()
        return "success"
        

        
    def startAdvertising(self):
        if (bleno.state == 'poweredOn'):            
            bleno.startAdvertising(socket.gethostname(), [blenoService.uuid])
   
    def stopAdvertising(self):
        bleno.stopAdvertising()
        if platform.system() == 'darwin':
            bleno.disconnect();

    def onStateChange(self,state):
        if state == 'poweredOn':
            Logger.info(LOCATION, 'Bluetooth powered on. Starting advertising...')
            BluetoothService.startAdvertising(self)
        else:
            Logger.info(LOCATION, 'Bluetooth is powered off. Stopping advertising...')
            BluetoothService.startAdvertising(self)
    
    def onAdvertisingStart(self,error):
        if error:
            Logger.error(LOCATION,'Failed to start advertising.')
        else:
            Logger.info(LOCATION, 'Successfully started advertising.')
        
        if not error:
            def on_setServiceError(error):
                if error:
                    Logger.error(LOCATION, 'setServices: ' , error)
                else:
                    Logger.info(LOCATION, 'Successfully set services.')
                
            bleno.setServices([blenoService])

