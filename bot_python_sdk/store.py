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
            with open(_actions_file_path, 'w') as outfile:
                outfile..write(json.dumps(actions))
        except IOError:
            Logger.error(LOCATION, 'Unable to write in '+_actions_file_path+' path')

    @staticmethod
    def get_actions():
        if not os.path.isfile(_actions_file_path):
            return []
        try:
            with open(_actions_file_path, 'r') as outfile:
                actions = json.loads(outfile.read())
                return actions
        except IOError:
            Logger.error(LOCATION, 'Unable to read in '+_actions_file_path+' path')
            return None


    @staticmethod
    def get_last_triggered(action_id):
        if not os.path.isfile(_last_triggered_file_path):
            return None
        try:
            with open(_last_triggered_file_path) as outfile:
                data = json.loads(outfile.read())
                return data[action_id] if action_id in data.keys() else None
        except IOError:
            Logger.error(LOCATION, 'Unable to read '+_last_triggered_file_path+' path')
            return None

    @staticmethod
    def set_last_triggered(action_id, time):
        data = {}
        if os.path.isfile(_last_triggered_file_path):
            with open(_last_triggered_file_path, 'r') as outfile:
                data = json.loads(outfile.read())
        data[action_id] = time
        try:
            with open(_last_triggered_file_path, 'w') as outfile:
                outfile.write(json.dumps(data))
        except IOError:
            Logger.error(LOCATION, 'Unable to write '+_last_triggered_file_path+' path')

    @staticmethod
    def save_qrcode(image):
        try:
            with open(_qr_image_path, 'wb') as outfile:
                image.save(outfile)
        except IOError:
            Logger.error(LOCATION, 'Unable to save image in '+_qr_image_path+' path')


    @staticmethod
    def get_configuration():
        try:
            with open(_configuration_file_path, 'r') as outfile:
                configuration = outfile.read()
                return json.loads(configuration)
        except IOError:
            Logger.error(LOCATION, 'Unable to read in '+_configuration_file_path+' path')
            return None

    @staticmethod
    def set_configuration(configuration):
        try:
            with open(_configuration_file_path, 'w') as outfile:
                 outfile.write(json.dumps(configuration))
        except IOError:
            Logger.error(LOCATION, 'Unable to write '+_configuration_file_path+' path')

    @staticmethod
    def has_configuration():
        return os.path.isfile(_configuration_file_path)

    @staticmethod
    def get_bot_public_key():
        try:
            with open(_bot_public_key) as outfile:
                public_key = outfile.read()
                return public_key
        except IOError:
            Logger.error(LOCATION, 'Unable to read in '+_bot_public_key+' path')
            return None
