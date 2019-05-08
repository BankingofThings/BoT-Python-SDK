from pybleno import *
import platform
import socket
from bot_python_sdk.logger import Logger
from bot_python_sdk.bleno.bleno_service import BlenoService

LOCATION = 'Bluetooth Service'
blenoService = BlenoService()
bleno = Bleno()

#Bluetooth Module
class BluetoothService:
    
    #Initializing the bluetooth module for state change and advertising
    def initialize(self):
        bleno.on('stateChange',self.onStateChange)
        bleno.on('advertisingStart', self.onAdvertisingStart)        
        bleno.start()

    #Checking the bluetooth state and start the advertising
    def startAdvertising(self):
        if (bleno.state == 'poweredOn'):            
            bleno.startAdvertising(socket.gethostname(), [blenoService.uuid])
       
    def stopAdvertising(self):
        bleno.stopAdvertising()
        if platform.system() == 'darwin':
            bleno.disconnect()

    #Advertising has been start and stop depends on the state
    def onStateChange(self,state):
        if state == 'poweredOn':
            Logger.info(LOCATION, 'Bluetooth powered on. Starting advertising...')
            BluetoothService.startAdvertising(self)
        else:
            Logger.info(LOCATION, 'Bluetooth is powered off. Stopping advertising...')
            BluetoothService.stopAdvertising(self)
    
    #Advertising start event will show status of advertising and set the service.
    #Characteristic will be set into the set service 
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
            bleno.setServices([blenoService], on_setServiceError)