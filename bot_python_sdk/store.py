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
    def __init__(self):
        pass

    @staticmethod
    def set_actions(actions):
        try:
            with open(_actions_file_path, 'w') as file:
                file.write(json.dumps(actions))
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to write in {0} path'.format(_actions_file_path))
            raise io_error.message

    @staticmethod
    def get_actions():
        if not os.path.isfile(_actions_file_path):
            return []
        try:
            with open(_actions_file_path, 'r') as file:
                actions = json.loads(file.read())
                return actions
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to read in {0} path'.format(_actions_file_path))
            raise io_error.message

    @staticmethod
    def get_last_triggered(action_id):
        if not os.path.isfile(_last_triggered_file_path):
            return None
        try:
            with open(_last_triggered_file_path) as file:
                data = json.loads(file.read())
                return data[action_id] if action_id in data.keys() else None
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to read {0} path'.format(_last_triggered_file_path))
            raise io_error.message

    @staticmethod
    def set_last_triggered(action_id, time):
        data = {}
        if os.path.isfile(_last_triggered_file_path):
            with open(_last_triggered_file_path, 'r') as file:
                data = json.loads(file.read())
        data[action_id] = time
        try:
            with open(_last_triggered_file_path, 'w') as file:
                file.write(json.dumps(data))
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to write {0} path'.format(_last_triggered_file_path))
            raise io_error.message

    @staticmethod
    def save_qrcode(image):
        try:
            with open(_qr_image_path, 'wb') as file:
                image.save(file)
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to save image in {0} path'.format(_qr_image_path))
            raise io_error.message

    @staticmethod
    def get_configuration():
        try:
            with open(_configuration_file_path, 'r') as file:
                configuration = file.read()
                return json.loads(configuration)
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to read in {0} path'.format(_configuration_file_path))
            raise io_error.message

    @staticmethod
    def set_configuration(configuration):
        try:
            with open(_configuration_file_path, 'w') as file:
                file.write(json.dumps(configuration))
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to write {0} path'.format(_configuration_file_path))
            raise io_error.message



    @staticmethod
    def has_configuration():
        return os.path.isfile(_configuration_file_path)

    @staticmethod
    def get_bot_public_key():
        try:
            with open(_bot_public_key) as file:
                public_key = file.read()
                return public_key
        except IOError as io_error:
            Logger.error(LOCATION, 'Unable to read in {0} path'.format(_bot_public_key))
            raise io_error.message
