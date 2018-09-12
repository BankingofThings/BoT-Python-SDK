import qrcode
from qrcode.image.pure import PymagingImage

from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.key_generator import KeyGenerator
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store

LOCATION = 'Configuration Service'
DEVICE_ID_KEY = 'deviceId'
DEVICE_STATUS_KEY = 'deviceStatus'
MAKER_ID_KEY = 'makerId'
PUBLIC_KEY_KEY = 'publicKey'
PRIVATE_KEY_KEY = 'privateKey'


class ConfigurationService:
    def __init__(self):
        self.configuration = Store.get_configuration()

    @staticmethod
    def has_configuration():
        return Store.has_configuration()

    @staticmethod
    def initialize_configuration(maker_id):
        Logger.info(LOCATION, 'Initializing configuration...')
        public_key, private_key = KeyGenerator().generate_key()
        configuration = {
            MAKER_ID_KEY: maker_id,
            DEVICE_ID_KEY: KeyGenerator.generate_uuid(),
            DEVICE_STATUS_KEY: DeviceStatus.NEW.value,
            PUBLIC_KEY_KEY: public_key,
            PRIVATE_KEY_KEY: private_key
        }
        Store.set_configuration(configuration)
        ConfigurationService.generate_qr_code(configuration)
        Logger.success(LOCATION, 'Configuration successfully initialized.')

    @staticmethod
    def generate_qr_code(configuration):
        Logger.info(LOCATION, 'Generating QR Code for alternative pairing...')
        image = qrcode.make(configuration, image_factory=PymagingImage)
        Store.save_qrcode(image)

    def get_device_info(self):
        return {
            DEVICE_ID_KEY: self.get_device_id(),
            MAKER_ID_KEY: self.get_maker_id(),
            PUBLIC_KEY_KEY: self._strip(self.get_public_key())
        }

    def set_device_status(self, device_status):
        self.configuration[DEVICE_STATUS_KEY] = device_status
        Store.set_configuration(self.configuration)

    def get_device_status(self):
        return self.configuration[DEVICE_STATUS_KEY]

    def get_public_key(self):
        return self.configuration[PUBLIC_KEY_KEY]

    def get_private_key(self):
        return self.configuration[PRIVATE_KEY_KEY]

    def get_maker_id(self):
        return self.configuration[MAKER_ID_KEY]

    def get_device_id(self):
        return self.configuration[DEVICE_ID_KEY]

    @staticmethod
    def _strip(string):
        string = string.replace('-----BEGIN RSA PUBLIC KEY-----\n', '')
        string = string.replace('-----END RSA PUBLIC KEY-----\n', '')
        return string
