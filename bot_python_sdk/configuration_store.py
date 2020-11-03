from bot_python_sdk.configuration import Configuration
from bot_python_sdk.device_status import DeviceStatus
from bot_python_sdk.store import Store

MAKER_ID = 'makerId'
DEVICE_ID = 'deviceId'
DEVICE_STATUS = 'deviceStatus'
PUBLIC_KEY = 'publicKey'
PRIVATE_KEY = 'privateKey'
ALTERNATIVE_ID = 'alternativeId'
BLUETOOTH_ENABLED = 'bluetoothEnabled'


# Store and fetch Configuration
class ConfigurationStore:

    def __init__(self):
        self.store = Store()

    def get(self):
        if self.store.has_configuration():
            dictionary = self.store.get_configuration()
            configuration = Configuration()
            configuration.initialize(
                dictionary[MAKER_ID],
                dictionary[DEVICE_ID],
                DeviceStatus[dictionary[DEVICE_STATUS]],
                dictionary[BLUETOOTH_ENABLED],
                dictionary[ALTERNATIVE_ID],
                dictionary[PUBLIC_KEY],
                dictionary[PRIVATE_KEY]
            )
            return configuration
        else:
            return Configuration()

    def save(self, configuration):
        self.store.set_configuration({
            MAKER_ID: configuration.get_maker_id(),
            DEVICE_ID: configuration.get_device_id(),
            DEVICE_STATUS: configuration.get_device_status(),
            PUBLIC_KEY: configuration.get_public_key(),
            PRIVATE_KEY: configuration.get_private_key(),
            ALTERNATIVE_ID: configuration.get_alternative_id(),
            BLUETOOTH_ENABLED: configuration.is_bluetooth_enabled()
        })
