import subprocess

import falcon

from bot_python_sdk.util.logger import Logger
from bot_python_sdk.data.storage import Storage


class PairingResource:
    def __init__(self):
        Logger.info('PairingResource', '__init__')

    def on_get(self, request, response):
        Logger.info('PairingResource', 'on_get')
        configuration = Storage.get_configuration_object()
        if configuration.get_is_paired():
            error = 'Device is already paired.'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
        device_information = configuration.get_device_information()
        response.media = falcon.json.dumps(device_information)
        subprocess.Popen(['make', 'pair'])
