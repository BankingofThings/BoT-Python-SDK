import json
import os
import subprocess

import falcon

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

INCOMING_REQUEST = 'Incoming request: '

DEVICE_ID_KEY = 'deviceId'
MAKER_ID_KEY = 'makerId'
PUBLIC_KEY_KEY = 'publicKey'

VALUE_KEY = 'value'
ALTERNATIVE_ID = 'alternativeID'

METHOD_GET = 'GET'
METHOD_POST = 'POST'
BASE_ENDPOINT = '/'
PAIRING_ENDPOINT = '/pairing'
ACTIVATION_ENDPOINT = '/activate'
QRCODE_ENDPOINT = '/qrcode'

QRCODE_IMG_PATH = 'storage/qr.png'


# TODO : Separate into file


# TODO : Separate into file
class PairingResource:
    def __init__(self):
        Logger.info(PairingResource.__name__, PairingResource.__init__.__name__)
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
        Logger.info(ActivationResource.__name__, ActivationResource.__init__.__name__)
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
        Logger.info(QRCodeResource.__name__, QRCodeResource.__init__.__name__)

    def on_get(self, request, response):
        Logger.info('api', "Serving QRCode Request...")
        stream = open(QRCODE_IMG_PATH, 'rb')
        content_length = os.path.getsize(QRCODE_IMG_PATH)
        response.content_type = "image/png"
        response.stream, response.content_length = stream, content_length


# Triggered by gunicorn
# Start Webserver and add supported endpoint resources
api = application = falcon.API()
api.add_route(PAIRING_ENDPOINT, PairingResource())
api.add_route(ACTIVATION_ENDPOINT, ActivationResource())
api.add_route(QRCODE_ENDPOINT, QRCodeResource())

Logger.info('api', 'init done')
# Start finn
Finn(api)
