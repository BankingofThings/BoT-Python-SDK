from bot_python_sdk.util.logger import Logger


# Sets the device status at CORE to active. In app aka Connected/Not connected.
# The CORE can set this status to false after some time interval. So do it everytime the device is powered on.
class ActiveDeviceService:
    def __init__(self, bot_service, device_id):
        Logger.info('ActiveDeviceService', '__init__')
        self.__bot_service = bot_service
        self.__device_id = device_id

    def execute(self):
        Logger.info('ActiveDeviceService', 'execute')
        try:
            self.__bot_service.post('status', {'deviceID': self.__device_id})
            Logger.info('ActiveDeviceService', 'run success')
            return True
        except Exception as e:
            Logger.info('ActiveDeviceService', 'run failed:' + str(e))
            return False
