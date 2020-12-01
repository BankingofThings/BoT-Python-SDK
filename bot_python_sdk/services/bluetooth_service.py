import platform
import socket

from pybleno import *

from bot_python_sdk.bleno.bleno_service import BlenoService
from bot_python_sdk.util.logger import Logger


###
# Bluetooth service class responsible for start/stop advertising, handling
# state chanegs, initialize the pybleno, register the necessay callbacks
# with pybleno to process the events from BLE stack.
# Important, install crypto package
##
class BluetoothService:

    # register event handlers with pybleno and start the bleno service
    def __init__(self):
        Logger.info('BluetoothService', '__init__')
        self.__bleno = Bleno()
        self.__bleno.setServices([BlenoService()], self.__on_set_services)
        self.__bleno.on('advertisingStart', self.__on_advertising_start)
        self.__bleno.on('stateChange', self.__on_state_change)
        Logger.info('BluetoothService', '__init__' + str(self.__bleno))
        self.__bleno.start()

    # start advertising depending on ble state (powered on/off)
    def __start_advertising(self):
        Logger.info('BluetoothService', 'start_advertising')
        if self.__bleno.state == 'poweredOn':
            self.__bleno.startAdvertising(socket.gethostname(), ['729BE9C4-3C61-4EFB-884F-B310B6FFFFD1'])

    # stop advertising
    def __stop_advertising(self):
        Logger.info('BluetoothService', 'stop_advertising')
        self.__bleno.stopAdvertising()
        if platform.system() == 'darwin':
            self.__bleno.disconnect()

    # handle state change events from BLE stack
    def __on_state_change(self, state):
        Logger.info('BluetoothService', 'on_state_change state = ' + str(state))

        if state == 'poweredOn':
            Logger.info('BluetoothService', 'Bluetooth powered on. Starting advertising...')
            self.__start_advertising()
        else:
            Logger.info('BluetoothService', 'Bluetooth is powered off. Stopping advertising...')
            self.__stop_advertising()

    '''
    handle advertising start notification from the BLE stack. On successful advertisement 
    set the custom bleno service and register the event handler.
    '''

    def __on_advertising_start(self, error):
        Logger.info('BluetoothService', 'on_advertising_start')

        if error:
            Logger.error('BluetoothService', 'Failed to start advertising.')
        else:
            Logger.info('BluetoothService', 'Successfully started advertising.')


    def __on_set_services(self, error):
        if error:
            Logger.error('BluetoothService', 'setServices: ' + error)
        else:
            Logger.info('BluetoothService', 'Successfully set services.')
