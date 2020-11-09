from pybleno import *
import platform
import socket
from bot_python_sdk.logger import Logger
from bot_python_sdk.bleno.bleno_service import BlenoService

LOCATION = 'Bluetooth Service'
# bleno service object
blenoService = BlenoService()
# bleno object creation
bleno = Bleno()

'''
Bluetooth service class responsible for start/stop advertising, handling 
state chanegs, initialize the pybleno, register the necessay callbacks
with pybleno to process the events from BLE stack.
'''


class BluetoothService:

    # register event handlers with pybleno and start the bleno service
    def initialize(self):
        bleno.onAdvertisingStart(self.on_advertising_start)
        bleno.onStateChange(self.on_state_change)
        bleno.start()

    # start advertising depending on ble state (powered on/off)
    def start_advertising(self):
        if (bleno.state == 'poweredOn'):
            bleno.startAdvertising(socket.gethostname(), ['729BE9C4-3C61-4EFB-884F-B310B6FFFFD1'])

    # stop advertising
    def stop_advertising(self):
        bleno.stopAdvertising()
        if platform.system() == 'darwin':
            bleno.disconnect()

    # handle state change events from BLE stack
    def on_state_change(self, state):
        if state == 'poweredOn':
            Logger.info(LOCATION, 'Bluetooth powered on. Starting advertising...')
            BluetoothService.start_advertising(self)
        else:
            Logger.info(LOCATION, 'Bluetooth is powered off. Stopping advertising...')
            BluetoothService.stop_advertising(self)

    '''
    handle advertising start notification from the BLE stack. On successful advertisement 
    set the custom bleno service and register the event handler.
    '''

    def on_advertising_start(self, error):
        if error:
            Logger.error(LOCATION, 'Failed to start advertising.')
        else:
            Logger.info(LOCATION, 'Successfully started advertising.')
        if not error:
            bleno.setServices([blenoService], self.on_set_services)

    def on_set_services(self, error):
        if error:
            Logger.error(LOCATION, 'setServices: ' + error)
        else:
            Logger.info(LOCATION, 'Successfully set services.')
