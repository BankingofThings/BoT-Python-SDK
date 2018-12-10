import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.logger import Logger

LOCATION = 'Pairing Service'
RESOURCE = 'pair'
POLLING_INTERVAL_IN_SECONDS = 5
MAXIMUM_TRIES = 3


class PairingService:

    def __init__(self):
        configuration = ConfigurationStore().get()
        self.maker_id = configuration.get_maker_id()
        self.device_id = configuration.get_device_id()
        self.bot_service = BoTService()

    def run(self):
        Logger.info(LOCATION, 'Starting to pair device...')
        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Pairing device, attempt: ' + str(tries))
            if self.pair():
                return True
            time.sleep(POLLING_INTERVAL_IN_SECONDS)
        return False

    def pair(self):
        response = self.bot_service.get(RESOURCE)
        paired = response.status is True
        if paired:
            Logger.success(LOCATION, 'Device successfully paired.')
        else:
            Logger.error(LOCATION, 'Failed pairing attempt.')
        return paired
