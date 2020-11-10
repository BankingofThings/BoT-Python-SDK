from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.logger import Logger


class Configuration:

    def __init__(self):
        self.product_id = ''
        self.device_id = ''
        self.device_status = DeviceStatus.NEW
        self.public_key = ''
        self.private_key = ''
        self.aid = ''
        self.bluetooth_enabled = True
        self.initialized = False

    def initialize(self, product_id, device_id, device_status, bluetooth_enabled, aid, public_key, private_key):
        self.product_id = product_id
        self.device_id = device_id
        self.device_status = device_status
        self.bluetooth_enabled = bluetooth_enabled
        self.aid = aid
        self.public_key = public_key
        self.private_key = private_key
        self.initialized = True

    def is_initialized(self):
        return self.initialized

    # Get the alternative ID
    def get_alternative_id(self):
        return self.aid

    def get_product_id(self):
        return self.product_id

    def get_device_id(self):
        return self.device_id

    def get_device_status(self):
        Logger.info('Configuration', 'get_device_status' + ' self.device_status = ' + str(self.device_status))
        return self.device_status

    def set_device_status(self, device_status):
        self.device_status = device_status

    def get_public_key(self):
        return self.public_key

    def get_stripped_public_key(self):
        stripped_public_key = self.public_key.replace('-----BEGIN RSA PUBLIC KEY-----\n', '')
        return stripped_public_key.replace('-----END RSA PUBLIC KEY-----\n', '')

    def get_private_key(self):
        return self.private_key

    def is_bluetooth_enabled(self):
        return self.bluetooth_enabled

    def get_device_information(self):
        data = {
            'deviceID': self.device_id,
            'makerID': self.product_id,
            'publicKey': self.get_stripped_public_key()
        }
        # Check if its multipairing mode and initialize the necessary data stuctures
        if self.device_status == DeviceStatus.MULTIPAIR:
            data['multipair'] = 1
            data['aid'] = self.aid
        return data

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.product_id,
            'deviceID': self.device_id
        }
