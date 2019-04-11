#if you have the issue “warning: setlocale: LC_ALL: cannot change locale (en_US.UTF-8)”, you can solve it with the command “sudo dpkg-reconfigure locales”, select en_US.UTF-8 as default


import json
import qrcode
from qrcode.image.pure import PymagingImage
from qrcode import QRCode

from bot_python_sdk.activation_service import ActivationService
from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.pairing_service import PairingService
from bot_python_sdk.store import Store

LOCATION = 'Configuration Service'


class ConfigurationService:
    
    def __init__(self):
        self.configuration_store = ConfigurationStore()
        self.configuration = self.configuration_store.get()
        self.key_generator = KeyGenerator()
    
    def initialize_configuration(self, maker_id):
        Logger.info(LOCATION, 'Initializing configuration...')
        public_key, private_key = KeyGenerator().generate_key()
        device_id = self.key_generator.generate_uuid()
        device_status = DeviceStatus.NEW.value
        self.configuration.initialize(maker_id, device_id, device_status, public_key, private_key)
        self.configuration_store.save(self.configuration)
        self.generate_qr_code()


    def generate_qr_code(self):
        try:
            device_information = self.configuration.get_device_information()
            qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
            qr.add_data(json.dumps(device_information))
            qr.print_ascii(invert=True)
        except Exception as exception:
            raise exception

configuration_service = ConfigurationService()
configuration_service.generate_qr_code()
