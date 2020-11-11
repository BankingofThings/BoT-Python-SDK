# TODO : Separate into file
import os

from bot_python_sdk.util.logger import Logger


class QRCodeResource(object):
    def __init__(self):
        Logger.info('QRCodeResource', '__init__')

    def on_get(self, request, response):
        Logger.info('QRCodeResource', 'on_get')
        stream = open('storage/qr.png', 'rb')
        content_length = os.path.getsize('/qrcode')
        response.content_type = "image/png"
        response.stream, response.content_length = stream, content_length