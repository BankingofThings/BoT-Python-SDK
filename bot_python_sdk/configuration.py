from bot_python_sdk.device_status import DeviceStatus


class Configuration:

    def __init__(self):
        self.maker_id = ''
        self.device_id = ''
        self.device_status = DeviceStatus.NEW
        self.public_key = ''
        self.private_key = ''
        self.initialized = False

    def is_initialized(self):
        return self.initialized

    def initialize(self, maker_id, device_id, device_status, public_key, private_key):
        self.maker_id = maker_id
        self.device_id = device_id
        self.device_status = device_status
        self.public_key = public_key
        self.private_key = private_key
        self.initialized = True

    def get_maker_id(self):
        return self.maker_id

    def get_device_id(self):
        return self.device_id

    def get_device_status(self):
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

    def get_device_information(self):
        return {
            'deviceID': self.device_id,
            'makerID': self.maker_id,
            'publicKey': self.get_stripped_public_key()
        }

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.maker_id,
            'deviceID': self.device_id
        }
