import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.logger import Logger

# PairingService.run() will start infinite loop with checking pair status at CORE
from bot_python_sdk.store import Store


class PairingService:

    def __init__(self):
        configuration = Store.get_configuration_object()
        self.maker_id = configuration.get_maker_id()
        self.device_id = configuration.get_device_id()
        self.device_status = configuration.get_device_status()
        self.bot_service = BoTService()

    def run(self):
        Logger.info('PairingService', 'PairingService.run')

        return self.__start_check_paired_loop()

    def __start_check_paired_loop(self):
        if self.__get_remote_paired_status():
            return True
        else:
            time.sleep(10)
            # restart after fail
            self.__start_check_paired_loop()

    def __get_remote_paired_status(self):
        Logger.info('PairingService', 'PairingService.get_remote_paired_status')

        try:
            response = self.bot_service.get("pair")
            Logger.info('PairingService', '__get_remote_paired_status response = ' + str(response))
            if response['status'] is True:
                Logger.info('PairingService', '__get_remote_paired_status Device successfully paired.')
                return True
            else:
                Logger.info('PairingService', '__get_remote_paired_status Failed pairing attempt.')
                return False
        # TODO : Make exception more specific
        except:
            Logger.info('PairingService', '__get_remote_paired_status')
            return False
