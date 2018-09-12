import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger

LOCATION = 'Activation Service'
RESOURCE = 'status'
DEVICE_ID_KEY = 'deviceID'
POLLING_INTERVAL_IN_SECONDS = 5
MAXIMUM_TRIES = 3


class ActivationService:

    def __init__(self):
        self.configuration_service = ConfigurationService()

    def run(self):
        Logger.info(LOCATION, 'Starting to activate device...')

        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Activating device, attempt: ' + str(tries))
            if self.activate():
                self.configuration_service.set_device_status(DeviceStatus.ACTIVE.value)
                break
            time.sleep(POLLING_INTERVAL_IN_SECONDS)

    def activate(self):
        try:
            BoTService().post(RESOURCE, {DEVICE_ID_KEY: self.configuration_service.get_device_id()})
            Logger.success(LOCATION, 'Device successfully activated. Triggering actions enabled.')
            return True
        except:
            Logger.error(LOCATION, 'Failed to activate device.')
            return False
