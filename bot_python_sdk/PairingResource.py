import subprocess

import falcon

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger


class PairingResource:
    def __init__(self, configuration_store):
        Logger.info('PairingResource', '__init__')
        self.configuration_store = configuration_store

    def on_get(self, request, response):
        Logger.info('PairingResource', 'on_get')
        configuration = self.configuration_store.get()
        if configuration.get_device_status() is not DeviceStatus.NEW:
            error = 'Device is already paired.'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
        device_information = configuration.get_device_information()
        response.media = falcon.json.dumps(device_information)
        subprocess.Popen(['make', 'pair'])
