import falcon
import json
import jwt
import requests

from requests_toolbelt.adapters.fingerprint import FingerprintAdapter

from bot_python_sdk.configuration_store import ConfigurationStore
from bot_python_sdk.logger import Logger
from bot_python_sdk.store import Store

LOCATION = 'BoT Service'
API_URL = 'https://iot.bankingofthings.io/'
SSL_FINGERPRINT = "76:E6:B6:DF:6D:3B:4D:2D:48:D1:B6:32:AD:D6:8E:80:53:3F:5F:88"
SERVICE_TAG = 'BoT Service: '
RESPONSE_DATA_KEY = 'bot'


class BoTService:

    def __init__(self):
        self.configuration = ConfigurationStore().get()

    def post(self, url, data):
        session = requests.Session()
        session.mount(API_URL, FingerprintAdapter(SSL_FINGERPRINT))
        try:
            response = session.post(
                API_URL + url,
                data=self._create_request_body(data),
                headers=self.configuration.get_headers()
            )
            if response.status_code < 200 or response.status_code >= 300:
                Logger.error(LOCATION, 'status: ' + str(response.status_code) + ', body: ' + response.text)
                raise falcon.HTTPServiceUnavailable
        except requests.exceptions.SSLError:
            self._handle_ssl_exception()
        except:
            Logger.error(LOCATION, 'Failed to POST resource.')
            raise falcon.HTTPServiceUnavailable

    def get(self, url):
        session = requests.Session()
        session.mount(API_URL, FingerprintAdapter(SSL_FINGERPRINT))
        try:
            response = session.get(API_URL + url, headers=self.configuration.get_headers())
            data = self._decode(response.text)
            if response.status_code < 200 or response.status_code >= 300:
                Logger.error(
                    LOCATION,
                    'status: ' + str(response.status_code) + ', body: ' + json.dumps(data)
                )
                raise falcon.HTTPServiceUnavailable
            return self._get_response(data)
        except requests.exceptions.SSLError:
            self._handle_ssl_exception()

    def _create_request_body(self, data):
        jwt_token = jwt.encode(
            {RESPONSE_DATA_KEY: data},
            self.configuration.get_private_key(),
            algorithm='RS256'
        ).decode('UTF-8')
        return json.dumps({RESPONSE_DATA_KEY: jwt_token})

    @staticmethod
    def _get_response(data):
        if RESPONSE_DATA_KEY not in data:
            Logger.error(LOCATION, 'Unexpected response format from BoT.' + json.dumps(data))
            raise falcon.HTTPInternalServerError
        return json.loads(data[RESPONSE_DATA_KEY])

    @staticmethod
    def _decode(token):
        try:
            data = jwt.decode(token, Store.get_bot_public_key(), algorithms=['RS256'])
        # TODO : Make exception more specific
        except:
            Logger.error(LOCATION, 'Could not decode message from BoT.')
            raise falcon.HTTPInternalServerError
        return data

    @staticmethod
    def _handle_ssl_exception():
        error = 'SSL Fingerprint verification failed. Could not verify server.'
        Logger.error(LOCATION, error)
        raise falcon.HTTPServiceUnavailable(description=error)
