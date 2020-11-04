# TODO : Separate into file
import os

from bot_python_sdk.logger import Logger


class QRCodeResource(object):
    def __init__(self):
        Logger.info(QRCodeResource.__name__, QRCodeResource.__init__.__name__)

    def on_get(self, request, response):
        Logger.info('api', "Serving QRCode Request...")
        stream = open('storage/qr.png', 'rb')
        content_length = os.path.getsize('/qrcode')
        response.content_type = "image/png"
        response.stream, response.content_length = stream, content_length