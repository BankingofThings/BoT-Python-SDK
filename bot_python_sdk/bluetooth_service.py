from pybleno import *
import platform
import socket
from bot_python_sdk.logger import Logger
from bot_python_sdk.bleno.bleno_service import BlenoService

LOCATION = 'Bluetooth Service'
#bleno service object
blenoService = BlenoService()
#bleno object creation
bleno = Bleno()

'''
Bluetooth service class responsible for start/stop advertising, handling 
state chanegs, initialize the pybleno, register the necessay callbacks
with pybleno to process the events from BLE stack.
'''
class BluetoothService:
    
    #register event handlers with pybleno and start the bleno service
    def initialize(self):
        bleno.on('stateChange',self.onStateChange)
        bleno.on('advertisingStart', self.onAdvertisingStart)        
        bleno.start()

    #start advertising depending on ble state (powered on/off)
    def startAdvertising(self):
        if (bleno.state == 'poweredOn'):            
            bleno.startAdvertising(socket.gethostname(), [blenoService.uuid])

    #stop advertising
    def stopAdvertising(self):
        bleno.stopAdvertising()
        if platform.system() == 'darwin':
            bleno.disconnect()

    #handle state change events from BLE stack
    def onStateChange(self,state):
        if state == 'poweredOn':
            Logger.info(LOCATION, 'Bluetooth powered on. Starting advertising...')
            BluetoothService.startAdvertising(self)
        else:
            Logger.info(LOCATION, 'Bluetooth is powered off. Stopping advertising...')
            BluetoothService.stopAdvertising(self)
    
    '''
    handle advertising start notification from the BLE stack. On successful advertisement 
    set the custom bleno service and register the event handler.
    '''
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
