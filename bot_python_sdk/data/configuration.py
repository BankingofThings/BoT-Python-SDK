class Configuration:

    def __init__(self):
        self.__product_id = ''
        self.__device_id = ''
        self.__public_key = ''
        self.__aid = ''
        self.__bluetooth_enabled = True
        self.__is_paired = False
        self.__is_multi_pair = False
        self.__initialized = False

    def initialize(self, product_id, device_id, is_multi_pair, bluetooth_enabled, aid, public_key):
        self.__product_id = product_id
        self.__device_id = device_id
        self.__is_multi_pair = is_multi_pair
        self.__bluetooth_enabled = bluetooth_enabled
        self.__aid = aid
        self.__public_key = public_key
        self.__initialized = True

    def is_initialized(self):
        return self.__initialized

    # Get the alternative ID
    def get_alternative_id(self):
        return self.__aid

    def get_product_id(self):
        return self.__product_id

    def get_device_id(self):
        return self.__device_id

    def get_is_paired(self):
        return self.__is_paired

    def set_is_paired(self, value):
        self.__is_paired = value

    def get_is_multi_pair(self):
        return self.__is_multi_pair

    def get_public_key(self):
        return self.__public_key

    def get_stripped_public_key(self):
        return self.__public_key.replace('-----BEGIN RSA PUBLIC KEY-----\n', '').replace('-----END RSA PUBLIC KEY-----\n', '')

    def is_bluetooth_enabled(self):
        return self.__bluetooth_enabled

    def get_device_information(self):
        data = {
            'deviceID': self.__device_id,
            'makerID': self.__product_id,
            'publicKey': self.get_stripped_public_key()
        }
        # Check if its multipairing mode and initialize the necessary data stuctures
        if self.__is_multi_pair:
            data['multipair'] = 1
            data['aid'] = self.__aid
        return data

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.__product_id,
            'deviceID': self.__device_id
        }
