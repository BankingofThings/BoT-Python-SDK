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

    def run(self):
        if not self.can_pair:
            return

        # Multipair device also needs at least one device to start.
        # if self.device_status == DeviceStatus.MULTIPAIR:
        #     Logger.info(LOCATION, 'Multipair mode, no need to poll or delete keys...')
        #     return

        Logger.info(LOCATION, 'Starting to pair device...')
        for tries in range(1, MAXIMUM_TRIES + 1):
            Logger.info(LOCATION, 'Pairing device, attempt: ' + str(tries))
            if self.pair():
                return True
            time.sleep(POLLING_INTERVAL_IN_SECONDS)
        return False

    def can_pair(self):
        return self.device_status == DeviceStatus.MULTIPAIR or self.device_status == DeviceStatus.NEW

    def pair(self):
        try:
            response = self.bot_service.get(RESOURCE)
            Logger.info(LOCATION, 'Pairing Response: 1' + str(response))
        # TODO : Make exception more specific
        except:
            Logger.error(LOCATION, 'Failed pairing attempt.')
            return False

        if response['status'] is True:
            Logger.success(LOCATION, 'Device successfully paired.')
            return True
        else:
            Logger.error(LOCATION, 'No device paired yet...Retrying after ' + POLLING_INTERVAL_IN_SECONDS + ' seconds')
            return False
