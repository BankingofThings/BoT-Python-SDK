import time

from bot_python_sdk.util.logger import Logger

# PairingService.run() will start infinite loop with checking pair status at CORE


class PairingService:

    def __init__(self, bot_service):
        self.bot_service = bot_service
        self.kill_loop = False

    def start(self):
        Logger.info('PairingService', 'run')

        return self.__start_check_paired_loop()

    def stop(self):
        Logger.info('PairingService', 'stop')

        self.kill_loop = True

    def __start_check_paired_loop(self):
        if self.kill_loop:
            return False
        elif self.__get_remote_paired_status():
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
        except Exception as e:
            Logger.info('PairingService', '__get_remote_paired_status error:' + str(e))
            return False