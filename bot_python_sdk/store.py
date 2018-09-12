import json
import os

_actions_file_path = 'storage/actions.json'
_last_triggered_file_path = 'storage/last_triggered.json'
_qr_image_path = 'storage/qr.png'
_configuration_file_path = 'storage/configuration.json'
_bot_public_key = 'storage/public.pem'


class Store:
    @staticmethod
    def set_actions(actions):
        file = open(_actions_file_path, 'w')
        file.write(json.dumps(actions))
        file.close()

    @staticmethod
    def get_actions():
        if not os.path.isfile(_actions_file_path):
            return False
        file = open(_actions_file_path, 'r')
        actions = json.loads(file.read())
        file.close()
        return actions

    @staticmethod
    def get_last_triggered(action_id):
        if not os.path.isfile(_last_triggered_file_path):
            return None
        file = open(_last_triggered_file_path)
        data = json.loads(file.read())
        file.close()
        return data[action_id] if action_id in data.keys() else None

    @staticmethod
    def set_last_triggered(action_id, time):
        data = {}
        if os.path.isfile(_last_triggered_file_path):
            file = open(_last_triggered_file_path, 'r')
            data = json.loads(file.read())
            file.close()
        data[action_id] = time
        file = open(_last_triggered_file_path, 'w')
        file.write(json.dumps(data))
        file.close()

    @staticmethod
    def save_qrcode(image):
        file = open(_qr_image_path, 'wb')
        image.save(file)
        file.close()

    @staticmethod
    def get_configuration():
        file = open(_configuration_file_path, 'r')
        configuration = file.read()
        file.close()
        return json.loads(configuration)

    @staticmethod
    def set_configuration(configuration):
        file = open(_configuration_file_path, 'w')
        file.write(json.dumps(configuration))
        file.close()

    @staticmethod
    def has_configuration():
        return os.path.isfile(_configuration_file_path)

    @staticmethod
    def get_bot_public_key():
        file = open(_bot_public_key)
        public_key = file.read()
        file.close()
        return public_key
