import time

import falcon

from bot_python_sdk.frequency import FrequenciesInSeconds
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


class ActionService:

    def __init__(self, configuration, bot_service):
        self.configuration = configuration
        self.bot_service = bot_service
        self.key_generator = KeyGenerator()
        self.store = Store()

    def get_actions(self):
        Logger.info('Action Service', 'Retrieving actions...')
        try:
            actions = self.bot_service.get('actions')
            Logger.success('Action Service', 'Successfully retrieved ' + str(actions) + ' action(s) from server')
            Store.set_actions(actions)
            return actions
        except falcon.HTTPServiceUnavailable:
            Logger.warning('Action Service', 'Unable to retrieve actions from server. Loading locally stored action(s)...')
            actions = self.store.get_actions()
            Logger.success('Action Service', 'Successfully loaded ' + str(len(actions)) + ' cached action(s)')
            return actions

    def trigger(self, action_id, value=None, alternative_id=None):
        Logger.info('Action Service', 'Triggering action: ' + action_id)
        action = self._get_action(action_id)
        self._validate_frequency(action)
        Logger.success('Action Service', 'Action valid')
        data = self._create_trigger_body(action_id, value, alternative_id)
        try:
            self.bot_service.post('actions', data)
            Logger.success('Action Service', 'Successfully triggered action: ' + action_id)
            self.store.set_last_triggered(action_id, time.time())
            return True
        # TODO : Make exception more specific
        except Exception as e:
            Logger.info('ActionService', 'trigger error:' + str(e))
            return False

    def _validate_frequency(self, action):
        last_triggered = self.store.get_last_triggered(action['actionID'])
        if last_triggered is None:
            return  # It was never triggered, so it is valid, unless we ever introduce Frequency: 'never'
        frequency = action['frequency']
        if frequency not in FrequenciesInSeconds.keys():
            self._handle_unsupported_frequency(frequency)

        if FrequenciesInSeconds[frequency] > time.time() - last_triggered:
            self._handle_maximum_frequency(frequency)

    def _get_action(self, action_id):
        actions = self.get_actions()
        for action in actions:
            if action['actionID'] == action_id:
                Logger.success('Action Service', 'Action found')
                return action
        Logger.error('Action Service', 'Action not found')
        raise falcon.HTTPNotFound(description='Action not found')

    def _create_trigger_body(self, action_id, value, alternative_id):
        data = {
            'actionID': action_id,
            'deviceID': self.configuration.get_device_id(),
            'queueID': self.key_generator.generate_uuid()
        }
        if alternative_id is not None:
            data['alternativeID'] = str(alternative_id)
        if value is not None:
            data['value'] = str(value)
        return data

    @staticmethod
    def _handle_unsupported_frequency(frequency):
        error = 'Frequency not supported: ' + frequency
        Logger.error('Action Service', error)
        raise falcon.HTTPBadRequest(description=error)

    @staticmethod
    def _handle_maximum_frequency(frequency):
        error = 'Maximum ' + frequency + ' triggers reached'
        Logger.error('Action Service', error)
        raise falcon.HTTPBadRequest(description=error)
