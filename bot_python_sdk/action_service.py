import falcon
import json
import time

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.frequency import Frequency, FrequenciesInSeconds
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store

LOCATION = 'Action Service'
ACTIONS_ENDPOINT = 'actions'

ACTION_ID_KEY = 'name'  # TODO Rename when renamed in Core
DEVICE_ID_KEY = 'deviceID'
FREQUENCY_KEY = 'frequency'
QUEUE_ID_KEY = 'queueID'
VALUE_KEY = 'value'


class ActionService:

    def __init__(self):
        self.configuration_service = ConfigurationService()

    def get_actions(self):
        Logger.info(LOCATION, 'Retrieving actions...')
        try:
            resource = ACTIONS_ENDPOINT + '/' + self.configuration_service.get_maker_id()
            actions = json.loads(BoTService.get(resource))
            Logger.success(LOCATION, 'Successfully retrieved ' + str(len(actions)) + ' action(s) from server')
            Store.set_actions(actions)
            return actions
        except falcon.HTTPServiceUnavailable:
            Logger.error(LOCATION, 'Unable to retrieve actions from server. Loading locally stored action(s)...')
            actions = Store.get_actions()
            Logger.success(LOCATION, 'Successfully loaded ' + str(len(actions)) + ' action(s) from server')
            return actions

    def trigger_action(self, action_id, value=None):
        Logger.info(LOCATION, 'Triggering action: ' + action_id)
        action = self._get_action(action_id)
        self._validate_frequency(action)
        Logger.success(LOCATION, 'Action valid')

        data = self.create_trigger_body(action_id, value)
        BoTService().post(ACTIONS_ENDPOINT, data)
        Logger.success(LOCATION, 'Successfully triggered action: ' + action_id)
        Store.set_last_triggered(action_id, time.time())

    def _validate_frequency(self, action):
        last_triggered = Store.get_last_triggered(action[ACTION_ID_KEY])
        if last_triggered is None:
            return  # It was never triggered, so it is valid
        frequency = action[FREQUENCY_KEY]
        if not Frequency.is_valid(frequency):
            self.handle_unsupported_frequency(frequency)

        if FrequenciesInSeconds[frequency] > time.time() - last_triggered:
            self.handle_maximum_frequency(frequency)

    def _get_action(self, action_id):
        actions = self.get_actions()
        for action in actions:
            if action[ACTION_ID_KEY] == action_id:
                Logger.success(LOCATION, 'Action found')
                return action
        Logger.error(LOCATION, 'Action not found')
        raise falcon.HTTPBadRequest(description='Action not found')

    def create_trigger_body(self, action_id, value):
        data = {
            ACTION_ID_KEY: action_id,
            DEVICE_ID_KEY: self.configuration_service.get_device_id(),
            QUEUE_ID_KEY: KeyGenerator.generate_uuid()
        }
        if value is not None:
            data[VALUE_KEY] = str(value)
        return data

    @staticmethod
    def handle_unsupported_frequency(frequency):
        error = 'Frequency not supported: ' + frequency
        Logger.error(LOCATION, error)
        raise falcon.HTTPForbidden(description=error)

    @staticmethod
    def handle_maximum_frequency(frequency):
        error = 'Maximum ' + frequency + ' triggers reached'
        Logger.error(LOCATION, error)
        raise falcon.HTTPForbidden(description=error)
