import time

from bot_python_sdk.activation_service import ActivationService
from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger

LOCATION = 'Pairing Service'
RESOURCE = 'pair'
POLLING_INTERVAL_IN_SECONDS = 5
MAXIMUM_TRIES = 3


class PairingService:

    def __init__(self):
        self.configuration_service = ConfigurationService()
        self.makerID = self.configuration_service.get_maker_id()
        self.deviceID = self.configuration_service.get_device_id()

    def run(self):
        Logger.info(LOCATION, 'Starting to pair device...')
        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Pairing device, attempt: ' + str(tries))
            if self.pair():
                self.configuration_service.set_device_status(DeviceStatus.PAIRED.value)
                ActivationService().run()
                break
            time.sleep(POLLING_INTERVAL_IN_SECONDS)

    def pair(self):
        response = BoTService.get(RESOURCE + '/' + self.makerID + '/' + self.deviceID)
        activated = response == 'true'
        if activated:
            Logger.success(LOCATION, 'Device successfully paired.')
        else:
            Logger.error(LOCATION, 'Failed pairing attempt.')
        return activated
