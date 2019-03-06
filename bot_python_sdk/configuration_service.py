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
        Logger.success(LOCATION, 'Configuration successfully initialized.')

    def resume_configuration(self):
        device_status = self.configuration.get_device_status()
        Logger.info(LOCATION, 'DeviceStatus = ' + device_status.value)
        if device_status == DeviceStatus.NEW:
            self.pair()
        if device_status == DeviceStatus.PAIRED:
            self.activate()

    def pair(self):
        success = PairingService().run()
        if success:
            self.configuration.set_device_status(DeviceStatus.PAIRED.value)
            self.configuration_store.save(self.configuration)
            self.activate()

    def activate(self):
        success = ActivationService().run()
        if success:
            self.configuration.set_device_status(DeviceStatus.ACTIVE.value)
            self.configuration_store.save(self.configuration)

    def generate_qr_code(self):
        try:
            Logger.info(LOCATION, 'Generating QR Code for alternative pairing...')
            device_information = self.configuration.get_device_information()
            image = qrcode.make(json.dumps(device_information), image_factory=PymagingImage)
            Store.save_qrcode(image)
            qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
            qr.add_data(json.dumps(device_information))
            qr.print_ascii(invert=True)
            Logger.success(LOCATION, 'QR Code successfully generated')
        except Exception as exception:
            Logger.error(LOCATION, 'QR Code not generated')
            raise exception
