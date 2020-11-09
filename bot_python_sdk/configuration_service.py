import json

import qrcode
from qrcode.image.pure import PymagingImage

from bot_python_sdk.activation_service import ActivationService
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_service import PairingService
from bot_python_sdk.store import Store


class ConfigurationService:

    # TODO Ercan:is this used?
    @staticmethod
    def resume_configuration():
        device_status = Store.get_device_status()

        Logger.info('ConfigurationService', 'resume_configuration' + ' device_status = ' + device_status.value)

        if device_status == DeviceStatus.NEW:
            ConfigurationService.pair()
        if device_status == DeviceStatus.PAIRED:
            ConfigurationService.activate()

    @staticmethod
    def pair():
        success = PairingService().run()
        if success:
            Store.set_device_status(DeviceStatus.PAIRED)
            ConfigurationService.activate()

    @staticmethod
    def activate():
        success = ActivationService().run()
        if success:
            Store.set_device_status(DeviceStatus.ACTIVE)

    @staticmethod
    def generate_qr_code():
        try:
            Store.save_qrcode(qrcode.make(json.dumps(Store.get_device_pojo()), image_factory=PymagingImage))
        except Exception as e:
            Logger.info('ConfigurationService', 'generate_qr_code error:' + str(e))
            raise e
