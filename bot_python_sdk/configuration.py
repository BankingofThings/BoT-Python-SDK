from bot_python_sdk.device_status import DeviceStatus
import json


class Configuration:

    def __init__(self):
        self.maker_id = ''
        self.device_id = ''
        self.device_status = DeviceStatus.NEW
        self.public_key = ''
        self.private_key = ''
        self.initialized = False
        self.aid=''

    def is_initialized(self):
        return self.initialized
    
    
    #Added alternative id for an initializing
    def initialize(self, maker_id, device_id, device_status, aid, public_key, private_key):
        self.maker_id = maker_id
        self.device_id = device_id
        self.device_status = device_status
        self.aid = aid
        self.public_key = public_key
        self.private_key = private_key
        self.initialized = True
    
    # Get the alternative ID
    def get_alternative_id(self):
        return self.aid

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
        data = {
                'deviceID': self.device_id,
                'makerID': self.maker_id,
                'publicKey': self.get_stripped_public_key()}
        
        # Check the device status if that is Multi pairing mode
        # add the additional required values for  Multipairing
        if(self.device_status == DeviceStatus.MULTIPAIR.value or self.device_status == DeviceStatus.MULTIPAIR):
            print('entered true block')
            data['multipair'] = 1
            data['aid'] = self.aid
            
        return data
        


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.maker_id,
            'deviceID': self.device_id
        }