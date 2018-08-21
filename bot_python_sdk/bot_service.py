import json
import jwt
import requests
import sys

sys.path.append('../')
from config import __private_key__, __maker_id__, __device_id__
from environment import __api_url__, __endpoint__


class BoTService:
    def activate(self):
        print('Sending pair request...')
        url = __api_url__ + __endpoint__ + '/pair/' + __maker_id__ + '/' + __device_id__
        response = requests.get(url)
        decoded = self._decode(response.text)
        return True if decoded['bot'] == 'true' else False

    def get_actions(self):
        print('Retrieving actions...')
        url = __api_url__ + __endpoint__ + '/actions/' + __maker_id__
        response = requests.get(url)
        decoded = self._decode(response.text)
        return json.loads(decoded['bot'])

    def trigger_action(self, action_id, value=None):
        print('Triggering action: ' + action_id)
        data = {'name': action_id, 'deviceID': __device_id__}  # TODO : remove deviceID once backend allows header only
        data['value'] = str(value) if value is not None else ''  # TODO : make value optional once backend allows it
        response = self._post(__api_url__ + __endpoint__ + '/actions', data)
        success = response.status_code == 200
        print('Action triggered' if success else 'Unable to trigger action')
        return success

    def _post(self, url, data):
        jwt_token = jwt.encode({'bot': data}, __private_key__, algorithm='RS256').decode('UTF-8')
        body = json.dumps({'bot': jwt_token})
        headers = {
            'Content-Type': 'application/json',
            'makerID': __maker_id__,
            'deviceID': __device_id__
        }
        return requests.post(url, data=body, headers=headers)

    def _decode(self, encoded_string):
        file = open('public.pem')
        public_key = file.read()
        file.close()
        return jwt.decode(encoded_string, public_key, algorithms=['RS256'])
