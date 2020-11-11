import time

import falcon

from bot_python_sdk.data.storage import Storage
from bot_python_sdk.util.key_generator import KeyGenerator
from bot_python_sdk.util.logger import Logger
from bot_python_sdk.util.pojo_converter import PojoConverter
from bot_python_sdk.util.utils import Utils


# getActions
# trigger
class ActionService:

    def __init__(self, configuration, bot_service, device_id):
        self.__configuration = configuration
        self.__bot_service = bot_service
        self.__device_id = device_id

    def __get_action_stored(self, action_id):
        for action in Storage.get_actions():
            if action['actionID'] == action_id:
                return action
        return None

    def get_actions(self):
        Logger.info('ActionService', 'Retrieving actions...')
        try:
            actions = self.__bot_service.get('actions')
            Logger.success('ActionService', 'Successfully retrieved ' + str(actions) + ' action(s) from server')
            Storage.set_actions(actions)
            return actions
        except falcon.HTTPServiceUnavailable:
            Logger.warning('ActionService', 'Unable to retrieve actions from server. Loading locally stored action(s)...')
            actions = Storage.get_actions()
            Logger.success('ActionService', 'Successfully loaded ' + str(len(actions)) + ' cached action(s)')
            return actions

    def trigger(self, action_id, value=None, alternative_id=None):
        Logger.info('ActionService', 'Triggering action: ' + action_id)
        action = self.__get_action_stored(action_id)

        action_validation_result = Utils.validate_frequency(action)
        if action_validation_result is 0:
            Logger.info('ActionService', 'trigger action can be triggered')
            data = PojoConverter.create_trigger_body(action_id, self.__device_id, KeyGenerator.generate_uuid(), alternative_id, value)
            try:
                self.__bot_service.post('actions', data)
                Logger.success('ActionService', 'Successfully triggered action: ' + action_id)
                Storage.set_last_triggered(action_id, time.time())
            except Exception as e:
                Logger.info('ActionService', 'trigger error:' + str(e))
        elif action_validation_result is 1:
            raise falcon.HTTPBadRequest(description='Frequency not supported')
        elif action_validation_result is 2:
            raise falcon.HTTPBadRequest(description='Maximum triggers reached')
        else:
            Logger.info('ActionService', 'trigger should never happen')
