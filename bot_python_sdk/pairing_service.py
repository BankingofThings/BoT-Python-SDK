import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.logger import Logger

LOCATION = 'Pairing Service'
RESOURCE = 'pair'
POLLING_INTERVAL_IN_SECONDS = 10
MAXIMUM_TRIES = 10


class PairingService:

    def __init__(self):
        configuration = ConfigurationStore().get()
        self.maker_id = configuration.get_maker_id()
        self.device_id = configuration.get_device_id()
        self.device_status = configuration.get_device_status()
        self.bot_service = BoTService()

    def start_check_paired_loop(self):
        if self.get_remote_paired_status():
            return True
        else:
            time.sleep(POLLING_INTERVAL_IN_SECONDS)
            # restart after fail
            self.start_check_paired_loop()

    def run(self):
        Logger.info(LOCATION, 'run()')

        return self.start_check_paired_loop()

    def get_remote_paired_status(self):
        Logger.info(PairingService.__name__, PairingService.get_remote_paired_status.__name__)

        try:
            response = self.bot_service.get(RESOURCE)
            Logger.info(LOCATION, 'Pairing Response: ' + str(response))
            if response['status'] is True:
                Logger.success(LOCATION, 'Device successfully paired.')
                return True
            else:
                Logger.error(LOCATION, 'Failed pairing attempt.')
                return False
        # TODO : Make exception more specific
        except:
            Logger.error(LOCATION, 'Failed pairing attempt.')
            return False
