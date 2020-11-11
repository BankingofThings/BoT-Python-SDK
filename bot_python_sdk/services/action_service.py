import time

import falcon

from bot_python_sdk.data.frequency import FrequenciesInSeconds
from bot_python_sdk.util.key_generator import KeyGenerator
from bot_python_sdk.util.logger import Logger
from bot_python_sdk.data.storage import Storage

# getActions
# trigger
from bot_python_sdk.util.pojo_converter import PojoConverter


class ActionService:

    def __init__(self, configuration, bot_service, device_id):
        self.__configuration = configuration
        self.__bot_service = bot_service
        self.__device_id = device_id

    def get_actions(self):
        Logger.info('Action Service', 'Retrieving actions...')
        try:
            actions = self.__bot_service.get('actions')
            Logger.success('Action Service', 'Successfully retrieved ' + str(actions) + ' action(s) from server')
            Storage.set_actions(actions)
            return actions
        except falcon.HTTPServiceUnavailable:
            Logger.warning('Action Service', 'Unable to retrieve actions from server. Loading locally stored action(s)...')
            actions = Storage.get_actions()
            Logger.success('Action Service', 'Successfully loaded ' + str(len(actions)) + ' cached action(s)')
            return actions

    def trigger(self, action_id, value=None, alternative_id=None):
        Logger.info('Action Service', 'Triggering action: ' + action_id)
        action = self.__get_action(action_id)
        self.__validate_frequency(action)
        Logger.success('Action Service', 'Action valid')
        data = PojoConverter.create_trigger_body(action_id, self.__device_id, KeyGenerator.generate_uuid(), alternative_id, value)
        try:
            self.__bot_service.post('actions', data)
            Logger.success('Action Service', 'Successfully triggered action: ' + action_id)
            Storage.set_last_triggered(action_id, time.time())
            return True
        # TODO : Make exception more specific
        except Exception as e:
            Logger.info('ActionService', 'trigger error:' + str(e))
            return False

    def __validate_frequency(self, action):
        last_triggered = Storage.get_last_triggered(action['actionID'])
        if last_triggered is None:
            return  # It was never triggered, so it is valid, unless we ever introduce Frequency: 'never'
        frequency = action['frequency']
        if frequency not in FrequenciesInSeconds.keys():
            self.__handle_unsupported_frequency(frequency)

        if FrequenciesInSeconds[frequency] > time.time() - last_triggered:
            self.__handle_maximum_frequency(frequency)

    def __get_action(self, action_id):
        actions = self.get_actions()
        for action in actions:
            if action['actionID'] == action_id:
                Logger.success('Action Service', 'Action found')
                return action
        Logger.error('Action Service', 'Action not found')
        raise falcon.HTTPNotFound(description='Action not found')

    @staticmethod
    def __handle_unsupported_frequency(frequency):
        error = 'Frequency not supported: ' + frequency
        Logger.error('Action Service', error)
        raise falcon.HTTPBadRequest(description=error)

    @staticmethod
    def __handle_maximum_frequency(frequency):
        error = 'Maximum ' + frequency + ' triggers reached'
        Logger.error('Action Service', error)
        raise falcon.HTTPBadRequest(description=error)
