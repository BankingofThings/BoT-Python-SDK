import falcon
import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.frequency import FrequenciesInSeconds
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store

LOCATION = 'Action Service'
ACTIONS_ENDPOINT = 'actions'

ACTION_ID = 'actionID'
DEVICE_ID = 'deviceID'
QUEUE_ID = 'queueID'
FREQUENCY = 'frequency'
VALUE = 'value'


class ActionService:

    def __init__(self):
        self.configuration = ConfigurationStore().get()
        self.bot_service = BoTService()
        self.key_generator = KeyGenerator()
        self.store = Store()

    def get_actions(self):
        Logger.info(LOCATION, 'Retrieving actions...')
        try:
            actions = self.bot_service.get(ACTIONS_ENDPOINT)
            Logger.success(LOCATION, 'Successfully retrieved ' + str(len(actions)) + ' action(s) from server')
            Store.set_actions(actions)
            return actions
        except falcon.HTTPServiceUnavailable:
            Logger.warning(LOCATION, 'Unable to retrieve actions from server. Loading locally stored action(s)...')
            actions = self.store.get_actions()
            Logger.success(LOCATION, 'Successfully loaded ' + str(len(actions)) + ' cached action(s)')
            return actions

    def trigger(self, action_id, value=None):
        Logger.info(LOCATION, 'Triggering action: ' + action_id)
        action = self._get_action(action_id)
        self._validate_frequency(action)
        Logger.success(LOCATION, 'Action valid')

        data = self.create_trigger_body(action_id, value)
        try:
            self.bot_service.post(ACTIONS_ENDPOINT, data)
            Logger.success(LOCATION, 'Successfully triggered action: ' + action_id)
            self.store.set_last_triggered(action_id, time.time())
            return True
        except:
            Logger.error(LOCATION, 'Unable to trigger action: ' + action_id)
            return False

    def _validate_frequency(self, action):
        last_triggered = self.store.get_last_triggered(action[ACTION_ID])
        if last_triggered is None:
            return  # It was never triggered, so it is valid, unless we ever introduce Frequency: 'never'
        frequency = action[FREQUENCY]
        if frequency not in FrequenciesInSeconds.keys():
            self._handle_unsupported_frequency(frequency)

        if FrequenciesInSeconds[frequency] > time.time() - last_triggered:
            self._handle_maximum_frequency(frequency)

    def _get_action(self, action_id):
        actions = self.get_actions()
        for action in actions:
            if action[ACTION_ID] == action_id:
                Logger.success(LOCATION, 'Action found')
                return action
        Logger.error(LOCATION, 'Action not found')
        raise falcon.HTTPBadRequest(description='Action not found')

    def create_trigger_body(self, action_id, value):
        data = {
            ACTION_ID: action_id,
            DEVICE_ID: self.configuration.get_device_id(),
            QUEUE_ID: self.key_generator.generate_uuid()
        }
        if value is not None:
            data[VALUE] = str(value)
        return data

    @staticmethod
    def _handle_unsupported_frequency(frequency):
        error = 'Frequency not supported: ' + frequency
        Logger.error(LOCATION, error)
        raise falcon.HTTPForbidden(description=error)

    @staticmethod
    def _handle_maximum_frequency(frequency):
        error = 'Maximum ' + frequency + ' triggers reached'
        Logger.error(LOCATION, error)
        raise falcon.HTTPForbidden(description=error)
