import falcon

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger

ACTION_ID = 'actionID'
METHOD_POST = 'POST'
ALTERNATIVE_ID = 'alternativeID'
ACTIONS_ENDPOINT = '/actions'
VALUE_KEY = 'value'

class ActionsResource:

    def __init__(self, action_service, configuration_store):
        self.action_service = action_service
        self.configuration_store = configuration_store

    def on_get(self, request, response):
        response.media = self.action_service.get_actions()

    def on_post(self, request, response):
        configuration = self.configuration_store.get()
        device_status = configuration.get_device_status()

        if device_status is not DeviceStatus.ACTIVE and device_status is not DeviceStatus.MULTIPAIR:
            error = 'Not allowed to trigger actions when device is not activated.'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)

        data = request.media
        if ACTION_ID not in data.keys():
            Logger.error('api', 'Missing parameter `' + ACTION_ID + '` for ' + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
            raise falcon.HTTPBadRequest

        if device_status is DeviceStatus.MULTIPAIR and ALTERNATIVE_ID not in data.keys():
            Logger.error('api', 'Missing parameter `' + ALTERNATIVE_ID + '` for ' + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
            raise falcon.HTTPBadRequest

        action_id = data[ACTION_ID]
        value = data[VALUE_KEY] if VALUE_KEY in data.keys() else None
        alternative_id = data[ALTERNATIVE_ID] if ALTERNATIVE_ID in data.keys() else None

        success = self.action_service.trigger(action_id, value, alternative_id)
        if success:
            response.media = {'message': 'Action triggered'}
        else:
            raise falcon.HTTPServiceUnavailable
