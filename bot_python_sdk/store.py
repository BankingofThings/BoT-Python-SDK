import json
import os


class Store:
    def store_actions(self, actions):
        file = open('actions.py', 'w')
        file.write(json.dumps(actions))
        file.close()

    def get_actions(self):
        if not os.path.isfile('actions.py'):
            return False
        file = open('actions.py', 'r')
        actions = json.loads(file.read())
        file.close()
        return actions

    def get_last_triggered(self, action_id):
        if not os.path.isfile('last_triggered.py'):
            return 'never'
        file = open('last_triggered.py')
        data = json.loads(file.read())
        file.close()
        return data[action_id] if action_id in data.keys() else 'never'

    def set_last_triggered(self, action_id, time):
        if not os.path.isfile('last_triggered.py'):
            data = {action_id: time}
            file = open('last_triggered.py', 'w')
            file.write(json.dumps(data))
        else:
            file = open('last_triggered.py', 'r')
            data = json.loads(file.read())
            file.close()
            data[action_id] = time
            file = open('last_triggered.py', 'w')
            file.write(json.dumps(data))
        file.close()

    def store_qrcode(self, image):
        file = open('qr.png', 'wb')
        image.save(file)
        file.close()

    def store_config(self, maker_id, uuid, private_key, public_key):
        file = open('config.py', 'w')
        file.write("__maker_id__='%s'\n__device_id__='%s'\n__private_key__='''%s'''\n__public_key__='''%s'''\n"
                   % (maker_id, uuid, private_key, public_key))
        file.close()

    def has_config(self):
        return os.path.isfile('config.py')
