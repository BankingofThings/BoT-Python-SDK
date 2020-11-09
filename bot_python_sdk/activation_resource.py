import falcon

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store


class ActivateDeviceResource:
    def __init__(self, bot_service):
        Logger.info('ActivationResource', '__init__')
        self.__bot_service = bot_service

    def execute(self):
        try:
            self.__bot_service.post('status', {'deviceID': Store.get_configuration_object().get_device_id()})
            Logger.info('ActivateDeviceService', 'run success')
            return True
        except Exception as e:
            Logger.info('ActivateDeviceService', 'run failed:' + str(e))
            return False

    # Executed after api call from above ActivateDeviceResource.execute
    def on_get(self, request, response):
        Logger.info('ActivationResource', 'on_get')
        configuration = Store.get_configuration_object()
        if configuration.get_device_status() is DeviceStatus.ACTIVE:
            error = 'Device is already activated'
            Logger.error('api', error)
            raise falcon.HTTPBadRequest(description=error)
