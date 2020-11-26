class Configuration:

    def __init__(self):
        self.product_id = ''
        self.device_id = ''
        self.public_key = ''
        self.aid = ''
        self.bluetooth_enabled = True
        self.is_paired = False
        self.is_multi_pair = False
        self.initialized = False

    def initialize(self, product_id, device_id, is_multi_pair, bluetooth_enabled, aid, public_key):
        self.product_id = product_id
        self.device_id = device_id
        self.is_multi_pair = is_multi_pair
        self.bluetooth_enabled = bluetooth_enabled
        self.aid = aid
        self.public_key = public_key
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

    def get_is_paired(self):
        return self.is_paired

    def get_is_multi_pair(self):
        return self.is_multi_pair

    def get_public_key(self):
        return self.public_key

    def get_stripped_public_key(self):
        return self.public_key.replace('-----BEGIN RSA PUBLIC KEY-----\n', '').replace('-----END RSA PUBLIC KEY-----\n', '')

    def is_bluetooth_enabled(self):
        return self.bluetooth_enabled

    def get_device_information(self):
        data = {
            'deviceID': self.device_id,
            'makerID': self.product_id,
            'publicKey': self.get_stripped_public_key()
        }
        # Check if its multipairing mode and initialize the necessary data stuctures
        if self.is_multi_pair:
            data['multipair'] = 1
            data['aid'] = self.aid
        return data

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.product_id,
            'deviceID': self.device_id
        }
