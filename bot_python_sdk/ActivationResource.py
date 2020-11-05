import falcon

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


class ActivationResource:
    def __init__(self):
        Logger.info('ActivationResource', 'ActivationResource.__init__')
        self.configuration_service = ConfigurationService()

    def on_get(self, request, response):
        Logger.info('api', "Serving Activation Request...")
        configuration = Store.get_configuration_object()
        if configuration.get_device_status() is DeviceStatus.ACTIVE:
            error = 'Device is already activated'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
        else:
            self.configuration_service.resume_configuration()