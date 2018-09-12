import falcon
import subprocess

from bot_python_sdk.action_service import ActionService
from bot_python_sdk.activation_service import ActivationService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_service import PairingService

LOCATION = 'Controller'
INCOMING_REQUEST_MESSAGE = 'Incoming request: '

ACTION_ID_KEY = 'actionID'
VALUE_KEY = 'value'

ACTIONS_ENDPOINT = '/actions'
PAIRING_ENDPOINT = '/pairing'


class ActionsResource:
    @staticmethod
    def on_get(request, response):
        Logger.info(LOCATION, INCOMING_REQUEST_MESSAGE + 'GET /actions')
        response.media = ActionService().get_actions()

    @staticmethod
    def on_post(request, response):
        if ConfigurationService().get_device_status() is not DeviceStatus.ACTIVE.value:
            error = 'Not allowed to trigger actions when device is not activated.'
            Logger.error(LOCATION, error)
            raise falcon.HTTPForbidden(description=error)
        Logger.info(LOCATION, INCOMING_REQUEST_MESSAGE + 'POST /actions')
        data = request.media
        if ACTION_ID_KEY not in data.keys():
            Logger.error(LOCATION, 'Missing parameter `actionID` for POST /actions')
            raise falcon.HTTPBadRequest

        action_id = data[ACTION_ID_KEY]
        value = data[VALUE_KEY] if VALUE_KEY in data.keys() else None

        ActionService().trigger_action(action_id, value)
        response.media = {'message': 'Action triggered'}


class PairingResource:
    @staticmethod
    def on_get(request, response):
        Logger.info(LOCATION, INCOMING_REQUEST_MESSAGE + 'GET /pairing')
        configuration_service = ConfigurationService()
        if configuration_service.get_device_status() is not DeviceStatus.NEW.value:
            Logger.error(LOCATION, 'Device is already paired.')
            raise falcon.HTTPForbidden(description='Device is already paired')
        response.media = configuration_service.get_device_info()
        subprocess.Popen(['make', 'pair'])


api = application = falcon.API()
api.add_route(ACTIONS_ENDPOINT, ActionsResource())
api.add_route(PAIRING_ENDPOINT, PairingResource())

# On startup resume pairing & activation process
deviceStatus = ConfigurationService().get_device_status()
if deviceStatus == DeviceStatus.NEW.value:
    Logger.info(LOCATION, 'DeviceStatus = NEW')
    PairingService().run()
if deviceStatus == DeviceStatus.PAIRED.value:
    Logger.info(LOCATION, 'DeviceStatus = PAIRED')
    ActivationService().run()
if deviceStatus == DeviceStatus.ACTIVE.value:
    Logger.success(LOCATION, 'DeviceStatus = ACTIVE')
