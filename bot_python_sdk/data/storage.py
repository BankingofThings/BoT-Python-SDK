import json
import os

from bot_python_sdk.data.configuration import Configuration
from bot_python_sdk.data.device_status import DeviceStatus
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
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

        try:
            if os.path.isfile(_qr_image_path):
                os.remove(_qr_image_path)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

        try:
            if os.path.isfile(_saved_actions_path):
                os.remove(_saved_actions_path)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

        try:
            if os.path.isfile(_last_triggered_path):
                os.remove(_last_triggered_path)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_bot_public_key():
        Logger.info('Store', 'get_bot_public_key')

        try:
            with open(_bot_public_key) as bot_file:
                public_key = bot_file.read()
                return public_key
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_configuration_object():
        dictionary = Storage.__get_configuration()
        configuration = Configuration()
        configuration.initialize(
            dictionary['makerId'],
            dictionary['deviceId'],
            DeviceStatus[dictionary['deviceStatus']],
            dictionary['bluetoothEnabled'],
            dictionary['alternativeId'],
            dictionary['publicKey'],
            dictionary['privateKey']
        )
        return configuration

    @staticmethod
    def save_configuration_object(configuration):
        __dictionary = {
            'makerId': configuration.get_product_id(),
            'deviceId': configuration.get_device_id(),
            'deviceStatus': configuration.get_device_status().value,
            'publicKey': configuration.get_public_key(),
            'privateKey': configuration.get_private_key(),
            'alternativeId': configuration.get_alternative_id(),
            'bluetoothEnabled': configuration.is_bluetooth_enabled()
        }
        Storage.__set_configuration(__dictionary)

    @staticmethod
    def get_device_status():
        return Storage.get_configuration_object().get_device_status()

    @staticmethod
    def set_device_status(device_status):
        configuration = Storage.get_configuration_object()

        configuration.set_device_status(device_status)

        Storage.save_configuration_object(configuration)

    @staticmethod
    def get_device_pojo():
        return Storage.get_configuration_object().get_device_information()