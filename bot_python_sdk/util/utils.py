import re
import time

import falcon

from bot_python_sdk.data.frequency import FrequenciesInSeconds
from bot_python_sdk.data.storage import Storage
from bot_python_sdk.util.logger import Logger


class Utils:
    # Function to validate the given IP Address
    @staticmethod
    def is_valid(ip):
        return re.search('''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)''', ip)

    # Check was previously triggered, if so check time is elapsed to be triggered again
    # @return 0 is valid, 1 and 2 are invalid
    @staticmethod
    def validate_frequency(action):
        last_triggered_time = Storage.get_last_triggered(action['actionID'])
        if last_triggered_time is not None:
            frequency = action['frequency']
            if frequency not in FrequenciesInSeconds.keys():
                Logger.info('Utils', 'validate_frequency not found:' + frequency)
                return 1
            elif FrequenciesInSeconds[frequency] > time.time() - last_triggered_time:
                return 2
            else:
                return 0
        else:
            return 0
