import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.logger import Logger

LOCATION = 'Activation Service'
RESOURCE = 'status'
DEVICE_ID = 'deviceID'
POLLING_INTERVAL_IN_SECONDS = 5
MAXIMUM_TRIES = 3


class ActivationService:

    def __init__(self):
        configuration = ConfigurationStore().get()
        self.device_id = configuration.get_device_id()
        self.bot_service = BoTService()

    def run(self):
        Logger.info(LOCATION, 'Starting to activate device...')
        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Activating device, attempt: ' + str(tries))
            if self.activate():
                return True
            time.sleep(POLLING_INTERVAL_IN_SECONDS)
        return False

    def activate(self):
        try:
            self.bot_service.post(RESOURCE, {DEVICE_ID: self.device_id})
            Logger.success(LOCATION, 'Device successfully activated. Triggering actions enabled.')
            return True
        except:
            Logger.error(LOCATION, 'Failed to activate device.')
            return False
