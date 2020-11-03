import json
import os
from bot_python_sdk.logger import Logger

_actions_file_path = 'storage/actions.json'
_last_triggered_file_path = 'storage/last_triggered.json'
_qr_image_path = 'storage/qr.png'
_configuration_file_path = 'storage/configuration.json'
_bot_public_key = 'storage/public.pem'
_saved_actions_path = 'storage/actions.json'
_last_triggered_path = 'storage/last_triggered.json'


# Storage manager
class Store:
        
    @staticmethod
    def set_actions(actions):
        Logger.info(Store.__name__, Store.set_actions.__name__)

        try:
            with open(_actions_file_path, 'w') as actions_file:
                actions_file.write(json.dumps(actions))
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_actions():
        Logger.info(Store.__name__, Store.get_actions.__name__)

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
        Logger.info(Store.__name__, Store.get_last_triggered.__name__)

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
        Logger.info(Store.__name__, Store.set_last_triggered.__name__)

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
        Logger.info(Store.__name__, Store.save_qrcode.__name__)

        try:
            with open(_qr_image_path, 'wb') as qr_image:
                image.save(qr_image)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_configuration():
        Logger.info(Store.__name__, Store.get_configuration.__name__)

        try:
            with open(_configuration_file_path, 'r') as configuration_file:
                configuration = configuration_file.read()
                return json.loads(configuration)
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def set_configuration(configuration):
        Logger.info(Store.__name__, Store.set_configuration.__name__)

        try:
            with open(_configuration_file_path, 'w') as configuration_file:
                configuration_file.write(json.dumps(configuration))
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def has_configuration():
        Logger.info(Store.__name__, Store.has_configuration.__name__)

        return os.path.isfile(_configuration_file_path)

    @staticmethod
    def remove_configuration():
        Logger.info(Store.__name__, Store.remove_configuration.__name__)

        try:
            if Store.has_configuration():
                os.remove(_configuration_file_path)
                if os.path.isfile(_qr_image_path):
                    os.remove(_qr_image_path)
                if os.path.isfile(_saved_actions_path):
                    os.remove(_saved_actions_path)
                if os.path.isfile(_last_triggered_path):
                    os.remove(_last_triggered_path)
                Logger.success('Store', 'Successfully reset device configuration')
            else:
                Logger.warning('Store', 'Could not reset, no configuration available')
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error

    @staticmethod
    def get_bot_public_key():
        Logger.info(Store.__name__, Store.get_bot_public_key.__name__)

        try:
            with open(_bot_public_key) as bot_file:
                public_key = bot_file.read()
                return public_key
        except IOError as io_error:
            Logger.error('Store', io_error.message)
            raise io_error
