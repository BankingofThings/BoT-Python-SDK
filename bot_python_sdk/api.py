import json
import os
import subprocess

import falcon

from bot_python_sdk.action_service import ActionService
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

INCOMING_REQUEST = 'Incoming request: '

DEVICE_ID_KEY = 'deviceId'
MAKER_ID_KEY = 'makerId'
PUBLIC_KEY_KEY = 'publicKey'

ACTION_ID = 'actionID'
VALUE_KEY = 'value'
ALTERNATIVE_ID = 'alternativeID'

METHOD_GET = 'GET'
METHOD_POST = 'POST'
BASE_ENDPOINT = '/'
ACTIONS_ENDPOINT = '/actions'
PAIRING_ENDPOINT = '/pairing'
ACTIVATION_ENDPOINT = '/activate'
QRCODE_ENDPOINT = '/qrcode'

QRCODE_IMG_PATH = 'storage/qr.png'

Logger.info('api', 'init start')

# TODO : Separate into file
class BaseResource(object):
    def __init__(self):
        pass

    def on_get(self, request, response):
        Logger.info('api', "Serving base endpoint request...")
        response.body = '{"message": "BoT-Python-SDK Webserver", "endpoints" : "/qrcode    /actions    /pairing    /activate" }'
        response.status = falcon.HTTP_200


# TODO : Separate into file
class ActionsResource:
    def __init__(self):
        self.action_service = ActionService()
        self.configuration_store = ConfigurationStore()

    def on_get(self, request, response):
        Logger.info('api', INCOMING_REQUEST + METHOD_GET + ' ' + ACTIONS_ENDPOINT)
        response.media = self.action_service.get_actions()

    def on_post(self, request, response):
        configuration = self.configuration_store.get()
        device_status = configuration.get_device_status()

        if device_status is not DeviceStatus.ACTIVE and device_status is not DeviceStatus.MULTIPAIR:
            error = 'Not allowed to trigger actions when device is not activated.'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)

        Logger.info('api', INCOMING_REQUEST + METHOD_POST + ' ' + ACTIONS_ENDPOINT)
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


# TODO : Separate into file
class PairingResource:
    def __init__(self):
        self.configuration_store = ConfigurationStore()

    def on_get(self, request, response):
        Logger.info('api', INCOMING_REQUEST + METHOD_GET + ' ' + PAIRING_ENDPOINT)
        configuration = self.configuration_store.get()
        if configuration.get_device_status() is not DeviceStatus.NEW:
            error = 'Device is already paired.'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
        device_information = configuration.get_device_information()
        response.media = json.dumps(device_information)
        subprocess.Popen(['make', 'pair'])


# TODO : Separate into file
class ActivationResource:
    def __init__(self):
        self.configuration_service = ConfigurationService()
        self.configuration_store = ConfigurationStore()

    def on_get(self, request, response):
        Logger.info('api', "Serving Activation Request...")
        configuration = self.configuration_store.get()
        if configuration.get_device_status() is DeviceStatus.ACTIVE:
            error = 'Device is already activated'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
        else:
            self.configuration_service.resume_configuration()


# TODO : Separate into file
class QRCodeResource(object):
    def __init__(self):
        pass

    def on_get(self, request, response):
        Logger.info('api', "Serving QRCode Request...")
        stream = open(QRCODE_IMG_PATH, 'rb')
        content_length = os.path.getsize(QRCODE_IMG_PATH)
        response.content_type = "image/png"
        response.stream, response.content_length = stream, content_length


# Triggered by gunicorn
# Start Webserver and add supported endpoint resources
api = application = falcon.API()
api.add_route(BASE_ENDPOINT, BaseResource())
api.add_route(ACTIONS_ENDPOINT, ActionsResource())
api.add_route(PAIRING_ENDPOINT, PairingResource())
api.add_route(ACTIVATION_ENDPOINT, ActivationResource())
api.add_route(QRCODE_ENDPOINT, QRCodeResource())

Logger.info('api', 'init done')

Finn().on_server_start_done()
