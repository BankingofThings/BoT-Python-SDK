import json
import os

from cryptography.fernet import Fernet

from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.util.logger import Logger

_actions_file_path = 'storage/actions.json'
_last_triggered_file_path = 'storage/last_triggered.json'
_qr_image_path = 'storage/qr.png'
_configuration_file_path = 'storage/configuration.json'
_bot_public_key = 'storage/public.pem'
_saved_actions_path = 'storage/actions.json'
_last_triggered_path = 'storage/last_triggered.json'


# Storage manager
class Storage:
    __aes_key_path = 'storage/key'
    __private_key_path = 'storage/pkey'

    @staticmethod
    def set_actions(actions):
        Logger.info('Store', 'set_actions')

        try:
            with open(_actions_file_path, 'w') as actions_file:
                actions_file.write(json.dumps(actions))
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_actions():
        Logger.info('Store', 'get_actions')

        if not os.path.isfile(_actions_file_path):
            return []
        try:
            with open(_actions_file_path, 'r') as actions_file:
                actions = json.loads(actions_file.read())
                return actions
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_last_triggered(action_id):
        Logger.info('Store', 'get_last_triggered')

        if not os.path.isfile(_last_triggered_file_path):
            return None
        try:
            with open(_last_triggered_file_path) as last_triggered_file:
                data = json.loads(last_triggered_file.read())
                return data[action_id] if action_id in data.keys() else None
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def set_last_triggered(action_id, time):
        Logger.info('Store', 'set_last_triggered')

        data = {}
        if os.path.isfile(_last_triggered_file_path):
            with open(_last_triggered_file_path, 'r') as last_triggered_file:
                data = json.loads(last_triggered_file.read())
        data[action_id] = time
        try:
            with open(_last_triggered_file_path, 'w') as last_triggered_file:
                last_triggered_file.write(json.dumps(data))
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def save_qrcode(image):
        Logger.info('Store', 'save_qrcode')

        try:
            with open(_qr_image_path, 'wb') as qr_image:
                image.save(qr_image)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    # Fetch storage data
    @staticmethod
    def __get_configuration():
        Logger.info('Store', 'get_configuration')

        try:
            return json.loads(open(_configuration_file_path, 'r').read())
        except IOError as e:
            Logger.error('Store', '__get_configuration error:' + str(e))
            raise e

    @staticmethod
    def __set_configuration(configuration):
        Logger.info('Store', 'set_configuration')

        try:
            open(_configuration_file_path, 'w').write(json.dumps(configuration))
        except IOError as io_error:
            Logger.error('Store', '__set_configuration:' + io_error.message)
            raise io_error

    @staticmethod
    def has_configuration():
        value = os.path.isfile(_configuration_file_path)
        Logger.info('Store', 'has_configuration ' + value.__str__())
        return value

    @staticmethod
    def remove_configuration():
        Logger.info('Store', 'remove_configuration')

        try:
            if os.path.isfile(_configuration_file_path):
                os.remove(_configuration_file_path)
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

        try:
            if os.path.isfile(_qr_image_path):
                os.remove(_qr_image_path)
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

        try:
            if os.path.isfile(_saved_actions_path):
                os.remove(_saved_actions_path)
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

        try:
            if os.path.isfile(_last_triggered_path):
                os.remove(_last_triggered_path)
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

        try:
            if os.path.isfile(Storage.__aes_key_path):
                Logger.info('Storage', 'remove_configuration key found and removed')
                os.remove(Storage.__aes_key_path)
        except IOError as e:
            Logger.info('Storage', 'remove_configuration key:' + str(e))
            raise e

        try:
            if os.path.isfile(Storage.__private_key_path):
                Logger.info('Storage', 'remove_configuration private key found and removed')
                os.remove(Storage.__private_key_path)
        except IOError as e:
            Logger.info('Storage', 'remove_configuration private key:' + str(e))
            raise e

    @staticmethod
    def get_bot_public_key():
        Logger.info('Store', 'get_bot_public_key')

        try:
            with open(_bot_public_key) as bot_file:
                public_key = bot_file.read()
                return public_key
        except IOError as e:
            Logger.info('Storage', 'get_bot_public_key' + str(e))
            raise e

    ###
    # Do only once
    ##
    @staticmethod
    def store_aes_key(key):
        Logger.info('Storage', 'store_aes_key')

        try:
            open(Storage.__aes_key_path, 'wb').write(key)
        except IOError as e:
            Logger.info('Storage', 'store_aes_key' + str(e))
            raise e

    @staticmethod
    def get_aes_key():
        Logger.info('Storage', 'get_aes_key')

        try:
            return open(Storage.__aes_key_path, "rb").read()
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

    ###
    # Encrypt string key and store as binary
    ##
    @staticmethod
    def store_private_key(key: str):
        Logger.info('Storage', 'store_private_key')

        try:
            open(Storage.__private_key_path, 'wb').write(Storage.encrypt(key))
        except IOError as e:
            Logger.info('Storage', 'store_aes_key' + str(e))
            raise e

    @staticmethod
    def get_private_key() -> str:
        Logger.info('Storage', 'get_private_key')

        try:
            return Storage.decrypt(open(Storage.__private_key_path, "rb").read())
        except IOError as e:
            Logger.error('Store', e.message)
            raise e

    @staticmethod
    def get_configuration_object():
        dictionary = Storage.__get_configuration()
        configuration = Configuration()
        configuration.initialize(
            dictionary['makerId'],
            dictionary['deviceId'],
            dictionary['isMultiPair'],
            dictionary['bluetoothEnabled'],
            dictionary['alternativeId'],
            dictionary['publicKey'])
        return configuration

    @staticmethod
    def save_configuration_object(configuration):
        dictionary = {
            'makerId': configuration.get_product_id(),
            'deviceId': configuration.get_device_id(),
            'isMultiPair': configuration.get_is_multi_pair(),
            'publicKey': configuration.get_public_key(),
            'alternativeId': configuration.get_alternative_id(),
            'bluetoothEnabled': configuration.is_bluetooth_enabled()
        }
        Storage.__set_configuration(dictionary)

    @staticmethod
    def get_device_pojo():
        return Storage.get_configuration_object().get_device_information()

    ###
    # Encrypt string by encoding to binary.
    ##
    @staticmethod
    def encrypt(data: str) -> bytes:
        return Fernet(Storage.get_aes_key()).encrypt(data.encode())

    ###
    # Decrypt encrypted binary data and decode to string.
    ##
    @staticmethod
    def decrypt(data: bytes) -> str:
        return Fernet(Storage.get_aes_key()).decrypt(data).decode()
        pass
