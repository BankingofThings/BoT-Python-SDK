import time
import bluetooth
from bluetooth.ble import DiscoveryService, BeaconService
from bot_python_sdk.logger import Logger

LOCATION = 'Bluetooth Service'



class BluetoothService:

    def discover_bluetooth_test(self):
        try:
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            print("found %d devices" % len(nearby_devices))

            for addr, name in nearby_devices:
                print("  %s - %s" % (addr, name))
            discover_response = {"message" : "success"}
        except Exception as exception:
            Logger.error(LOCATION, 'Failed discover_bluetooth_test')
            discover_response = {"message" : "failed"}
            raise exception        
        return discover_response

    def discover_ble_test(self):
        try:
            service = DiscoveryService()
            devices = service.discover(2)
            for address, name in devices.items():
                print("name: {}, address: {}".format(name, address))
            discover_response = {"message" : "success"}
        except Exception as exception:
            Logger.error(LOCATION, 'Failed discover_ble_test')
            discover_response = {"message" : "failed"}
            raise exception
        return discover_response


    def advertising_ble_test(self):
        try:
            service = BeaconService()
            service.start_advertising("729BE9C4-3C61-4EFB-884F-B310B6FFFFD1",
               1, 1, 1, 200)
            time.sleep(15)
            service.stop_advertising()
            print("Done.")
            advertising_response = {"message" : "success"}
        except:
            Logger.error(LOCATION, 'Failed advertising_ble_test')
            advertising_response = {"message" : "failed"}
             raise exception
        return advertising_response







