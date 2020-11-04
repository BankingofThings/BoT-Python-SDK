# TODO : Separate into file
import falcon

from bot_python_sdk.logger import Logger


class BaseResource(object):
    def __init__(self):
        Logger.info(BaseResource.__name__, BaseResource.__init__.__name__)

    def on_get(self, request, response):
        Logger.info('api', "Serving base endpoint request...")
        response.body = '{"message": "BoT-Python-SDK Webserver", "endpoints" : "/qrcode    /actions    /pairing    /activate" }'
        response.status = falcon.HTTP_200