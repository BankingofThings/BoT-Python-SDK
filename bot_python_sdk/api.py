import falcon
import qrcode
import sys
import subprocess

from bot_python_sdk.bot_service import BoTService
from bot_python_sdk.store import Store
from bot_python_sdk.trigger import Trigger
from qrcode.image.pure import PymagingImage

sys.path.append('../')
import config


class TriggerResource:
    def on_post(self, request, response):
        data = request.media
        if not 'actionID' in data.keys():
            response.status = falcon.HTTP_BAD_REQUEST
            response.media = {"message": "Missing parameter 'actionID'"}
            return
        action_id = data['actionID']
        value = data['value'] if 'value' in data.keys() else None

        trigger = Trigger(action_id, value)

        if not trigger.frequency_is_valid():
            response.status = falcon.HTTP_BAD_REQUEST
            response.media = {'message': 'Unable to trigger action. Maximum frequency reached.'}
            return

        success = trigger.send()
        if success:
            response.status = falcon.HTTP_CREATED
            response.media = {'message': 'Action triggered'}
        else:
            response.status = falcon.HTTP_METHOD_NOT_ALLOWED
            response.media = {'message': 'Unable to trigger action'}


class ActionsResource:
    def on_get(self, request, response):
        actions = BoTService().get_actions()
        Store().store_actions(actions)
        print(actions)
        response.media = actions


class PairingResource:
    def on_get(self, request, response):
        subprocess.Popen(['make', 'activate'])
        data = {
            "device_id": config.__device_id__,
            "maker_id": config.__maker_id__,
            "public_key": self.strip(config.__public_key__)
        }
        image = qrcode.make(data, image_factory=PymagingImage)
        Store().store_qrcode(image)
        response.media = data

    def strip(self, string):
        string = string.replace('-----BEGIN RSA PUBLIC KEY-----\n', '')
        string = string.replace('-----END RSA PUBLIC KEY-----\n', '')
        return string


api = falcon.API()
api.add_route('/', TriggerResource())
api.add_route('/actions', ActionsResource())
api.add_route('/pairing', PairingResource())
