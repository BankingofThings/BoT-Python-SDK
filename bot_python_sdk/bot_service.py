import falcon
import json
import jwt
import requests

from requests_toolbelt.adapters.fingerprint import FingerprintAdapter

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store

LOCATION = 'BoT Service'
API_URL = 'https://api.bankingofthings.io/bot_iot/'
SSL_FINGERPRINT = "98:67:D8:29:37:E3:8C:2D:44:D5:C4:21:4B:D7:CB:DF:59:7A:CE:61"
SERVICE_TAG = 'BoT Service: '
RESPONSE_DATA_KEY = 'bot'


class BoTService:

    def __init__(self):
        self.configurationService = ConfigurationService()

    def post(self, url, data):
        session = requests.Session()
        session.mount(API_URL, FingerprintAdapter(SSL_FINGERPRINT))
        try:
            response = session.post(
                API_URL + url,
                data=self._create_request_body(data),
                headers=self._create_request_headers()
            )
            if response.status_code < 200 or response.status_code >= 300:
                Logger.error(LOCATION, 'status: ' + response.status_code + ', body: ' + response.text)
                raise falcon.HTTPServiceUnavailable
        except requests.exceptions.SSLError:
            self._handle_ssl_exception()
        except:
            Logger.error(LOCATION, 'Failed to POST resource.')
            raise falcon.HTTPServiceUnavailable

    @staticmethod
    def get(url):
        session = requests.Session()
        session.mount(API_URL, FingerprintAdapter(SSL_FINGERPRINT))
        try:
            response = session.get(API_URL + url)
            if response.status_code < 200 or response.status_code >= 300:
                Logger.error(LOCATION, 'status: ' + response.status_code + ', body: ' + response.text)
                raise falcon.HTTPServiceUnavailable
            return BoTService._decode(response.text)
        except requests.exceptions.SSLError:
            BoTService._handle_ssl_exception()
        except:
            Logger.error(LOCATION, 'Failed to GET resource.')
            raise falcon.HTTPServiceUnavailable

    def _create_request_body(self, data):
        jwt_token = jwt.encode(
            {RESPONSE_DATA_KEY: data},
            self.configurationService.get_private_key(),
            algorithm='RS256'
        ).decode('UTF-8')
        return json.dumps({RESPONSE_DATA_KEY: jwt_token})

    def _create_request_headers(self):
        return {
            'Content-Type': 'application/json',
            'makerID': self.configurationService.get_maker_id(),
            'deviceID': self.configurationService.get_device_id()
        }

    @staticmethod
    def _decode(token):
        try:
            data = jwt.decode(token, Store.get_bot_public_key(), algorithms=['RS256'])
        except:
            Logger.error(LOCATION, 'Could not decode message from BoT.')
            raise falcon.HTTPInternalServerError
        if RESPONSE_DATA_KEY not in data:
            Logger.error(LOCATION, 'Unexpected response format from BoT.')
            raise falcon.HTTPInternalServerError
        return data[RESPONSE_DATA_KEY]

    @staticmethod
    def _handle_ssl_exception():
        error = 'SSL Fingerprint verification failed. Could not verify server.'
        Logger.error(LOCATION, error)
        raise falcon.HTTPServiceUnavailable(description=error)
