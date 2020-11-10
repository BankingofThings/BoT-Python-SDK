import falcon

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


class ActionsResource:

    def __init__(self, action_service):
        self.action_service = action_service

    def on_get(self, request, response):
        Logger.info('ActionsResource', 'on_get')
        response.media = self.action_service.get_actions()

    def on_post(self, request, response):
        Logger.info('ActionsResource', 'on_post')
        configuration = Store.get_configuration_object()
        device_status = configuration.get_device_status()

        data = request.media

        if 'actionID' not in data.keys():
            Logger.error('api', 'Missing parameter `' + 'actionID' + '` for ' + 'POST' + ' ' + '/actions')
            raise falcon.HTTPBadRequest

        if device_status is DeviceStatus.MULTIPAIR and 'alternativeID' not in data.keys():
            Logger.error('api', 'Missing parameter `' + 'alternativeID' + '` for ' + 'POST' + ' ' + '/actions')
            raise falcon.HTTPBadRequest

        action_id = data['actionID']
        value = data['value'] if 'value' in data.keys() else None
        alternative_id = data['alternativeID'] if 'alternativeID' in data.keys() else None

        success = self.action_service.trigger(action_id, value, alternative_id)
        if success:
            response.media = {'message': 'Action triggered'}
        else:
            raise falcon.HTTPServiceUnavailable
