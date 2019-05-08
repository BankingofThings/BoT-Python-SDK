import falcon
import subprocess
import json
from bot_python_sdk.action_service import ActionService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger

from bot_python_sdk.bluetooth_service import BluetoothService

LOCATION = 'Controller'
INCOMING_REQUEST = 'Incoming request: '

DEVICE_ID_KEY = 'deviceId'
MAKER_ID_KEY = 'makerId'
PUBLIC_KEY_KEY = 'publicKey'

ACTION_ID = 'actionID'
VALUE_KEY = 'value'

METHOD_GET = 'GET'
METHOD_POST = 'POST'
ACTIONS_ENDPOINT = '/actions'
PAIRING_ENDPOINT = '/pairing'
ACTIVATION_ENDPOINT = '/activation'


class ActionsResource:
    def __init__(self):
        self.action_service = ActionService()
        self.configuration_store = ConfigurationStore()

    def on_get(self, request, response):
        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_GET + ' ' + ACTIONS_ENDPOINT)
        response.media = self.action_service.get_actions()

    def on_post(self, request, response):
        configuration = self.configuration_store.get()

        if configuration.get_device_status() is not DeviceStatus.ACTIVE:
            error = 'Not allowed to trigger actions when device is not activated.'
            Logger.error(LOCATION, error)
            raise falcon.HTTPForbidden(description=error)

        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
        data = request.media
        if ACTION_ID not in data.keys():
            Logger.error(LOCATION, 'Missing parameter `' + ACTION_ID + '` for ' + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
            raise falcon.HTTPBadRequest

        action_id = data[ACTION_ID]
        value = data[VALUE_KEY] if VALUE_KEY in data.keys() else None

        success = self.action_service.trigger(action_id, value)
        if success:
            response.media = {'message': 'Action triggered'}
        else:
            raise falcon.HTTPServiceUnavailable


class PairingResource:
    def __init__(self):
        self.configuration_store = ConfigurationStore()

    def on_get(self, request, response):
        Logger.info(LOCATION, INCOMING_REQUEST + METHOD_GET + ' ' + PAIRING_ENDPOINT)
        configuration = self.configuration_store.get()
        if configuration.get_device_status() is not DeviceStatus.NEW:
            error = 'Device is already paired.'
            Logger.error(LOCATION, error)
            raise falcon.HTTPForbidden(description=error)
        device_information = configuration.get_device_information()
        response.media = json.dumps(device_information)
        subprocess.Popen(['make', 'pair'])


class ActivationResource:
    def __init__(self):
        self.configuration_service = ConfigurationService()

    def on_get(self):
        self.configuration_service.resume_configuration()
        
        
api = application = falcon.API()
api.add_route(ACTIONS_ENDPOINT, ActionsResource())
api.add_route(PAIRING_ENDPOINT, PairingResource())
api.add_route(ACTIVATION_ENDPOINT, ActivationResource())

ConfigurationService().resume_configuration()

#Initialize the Bluetooth service class to process
#handle BLE specific envents and callbacks
BluetoothService().initialize()
