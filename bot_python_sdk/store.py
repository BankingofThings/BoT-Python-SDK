import json
import os
from bot_python_sdk.logger import Logger

_actions_file_path = 'storage/actions.json'
_last_triggered_file_path = 'storage/last_triggered.json'
_qr_image_path = 'storage/qr.png'
_configuration_file_path = 'storage/configuration.json'
_bot_public_key = 'storage/public.pem'

LOCATION = 'Store'


class Store:
    @staticmethod
    def set_actions(actions):
        try:
            with open(_actions_file_path, 'w') as actions_file:
                actions_file.write(json.dumps(actions))
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def get_actions():
        if not os.path.isfile(_actions_file_path):
            return []
        try:
            with open(_actions_file_path, 'r') as actions_file:
                actions = json.loads(actions_file.read())
                return actions
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def get_last_triggered(action_id):
        if not os.path.isfile(_last_triggered_file_path):
            return None
        try:
            with open(_last_triggered_file_path) as last_triggered_file:
                data = json.loads(last_triggered_file.read())
                return data[action_id] if action_id in data.keys() else None
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def set_last_triggered(action_id, time):
        data = {}
        if os.path.isfile(_last_triggered_file_path):
            with open(_last_triggered_file_path, 'r') as last_triggered_file:
                data = json.loads(last_triggered_file.read())
        data[action_id] = time
        try:
            with open(_last_triggered_file_path, 'w') as last_triggered_file:
                last_triggered_file.write(json.dumps(data))
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def save_qrcode(image):
        try:
            with open(_qr_image_path, 'wb') as qr_image:
                image.save(qr_image)
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def get_configuration():
        try:
            with open(_configuration_file_path, 'r') as configuration_file:
                configuration = configuration_file.read()
                return json.loads(configuration)
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def set_configuration(configuration):
        try:
            with open(_configuration_file_path, 'w') as configuration_file:
                configuration_file.write(json.dumps(configuration))
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def has_configuration():
        return os.path.isfile(_configuration_file_path)

    @staticmethod
    def remove_configuration():
        try:
            if Store.has_configuration():
                os.remove(_configuration_file_path)
                os.remove(_qr_image_path)
                Logger.success(LOCATION, 'Successfully removed configuration file')
            else:
                Logger.warning(LOCATION, 'Could not reset, no configuration available')
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error

    @staticmethod
    def get_bot_public_key():
        try:
            with open(_bot_public_key) as bot_file:
                public_key = bot_file.read()
                return public_key
        except IOError as io_error:
            Logger.error(LOCATION, io_error.message)
            raise io_error
