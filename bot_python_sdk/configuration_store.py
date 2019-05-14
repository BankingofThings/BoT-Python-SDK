from bot_python_sdk.configuration import Configuration
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.store import Store
import json

MAKER_ID = 'makerId'
DEVICE_ID = 'deviceId'
DEVICE_STATUS = 'deviceStatus'
PUBLIC_KEY = 'publicKey'
PRIVATE_KEY = 'privateKey'
#Added alternative id for JSON field name
ALTERNATIVE_ID = 'alternativeId'


class ConfigurationStore:
    def __init__(self):
        self.store = Store()

    def get(self):
        configuration = Configuration()
        if not self.store.has_configuration():
            return configuration
        dictionary = self.store.get_configuration()
        return self._to_configuration(dictionary)
    
    # Generating the JSON file
    def save(self, configuration):
        dictionary = self._to_dictionary(configuration)
        self.store.set_configuration(dictionary)
        
    
    @staticmethod
    def _to_dictionary(configuration):
        
        return {
                MAKER_ID: configuration.get_maker_id(),
                DEVICE_ID: configuration.get_device_id(),
                DEVICE_STATUS: configuration.get_device_status(),
                PUBLIC_KEY: configuration.get_public_key(),
                PRIVATE_KEY: configuration.get_private_key(),
                #Added alternative id as a field in json fine
                ALTERNATIVE_ID: configuration.get_alternative_id()
            }

    @staticmethod
    
    def _to_configuration(dictionary):
        configuration = Configuration()   
        configuration.initialize(
            dictionary[MAKER_ID],
            dictionary[DEVICE_ID],
            DeviceStatus[dictionary[DEVICE_STATUS]],
            # passing the dictionary of alternative value for initialization 
            dictionary[ALTERNATIVE_ID],
            dictionary[PUBLIC_KEY],
            dictionary[PRIVATE_KEY]
        )
        return configuration

