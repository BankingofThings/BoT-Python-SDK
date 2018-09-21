import json
import requests


class Example:
    def pairing(self):
        requests.get('localhost:3001/pairing')

    def get_actions(self):
        requests.get('localhost:3001/actions')

    def post_action(self):
        url = 'localhost:3001/actions'
        body = {'actionID': 'YOUR_ACTION_ID'}
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(body), headers=headers)
