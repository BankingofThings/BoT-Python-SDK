import falcon
import json
import jwt
import requests

from requests_toolbelt.adapters.fingerprint import FingerprintAdapter

from bot_python_sdk.util.logger import Logger
from bot_python_sdk.data.storage import Storage

API_URL = 'https://iot-dev.bankingofthings.io/'
SSL_FINGERPRINT = "3E:18:EE:35:DF:CA:35:D7:4B:FB:4E:AB:9F:A1:B5:7A:2D:91:8D:1F"
RESPONSE_DATA_KEY = 'bot'


class BoTService:

    def __init__(self, private_key, headers):
        Logger.info('BoTService', '__init__ ' + API_URL)
        self.__private_key = private_key
        self.__headers = headers

    def post(self, url, data):
        try:
            response = self.__create_session().post(API_URL + url, data=self.__create_request_body(data), headers=self.__headers)
            Logger.info('BoTService', 'post response:' + str(response))
            if response.status_code < 200 or response.status_code >= 300:
                raise falcon.HTTPServiceUnavailable
        except requests.exceptions.SSLError:
            self.__handle_ssl_exception()
        except Exception as e:
            Logger.info('BoTService', 'post error:' + str(e))
            raise falcon.HTTPServiceUnavailable

    def get(self, url):
        try:
            response = self.__create_session().get(API_URL + url, headers=self.__headers)
            Logger.info('BoTService', 'get response = ' + str(response))
            if response.status_code < 200 or response.status_code >= 300:
                raise falcon.HTTPServiceUnavailable
            else:
                try:
                    # get data part of jwt
                    data = jwt.decode(response.text, Storage.get_bot_public_key(), algorithms=['RS256'])
                    # check data part has bot object
                    if RESPONSE_DATA_KEY in data:
                        return json.loads(data[RESPONSE_DATA_KEY])
                    else:
                        Logger.info('BoTService', '__get_response error: bot object not found')
                        return data
                except Exception as e:
                    Logger.info('BoTService', '__get_response error: jwt decoding failed = ' + str(e))
                    return response.text
        except requests.exceptions.SSLError:
            self.__handle_ssl_exception()
        except Exception as e:
            Logger.info('BoTService', 'get error:' + str(e))
            raise falcon.HTTPServiceUnavailable

    def __create_request_body(self, data):
        jwt_token = jwt.encode({RESPONSE_DATA_KEY: data}, self.__private_key, algorithm='RS256').decode('UTF-8')
        return json.dumps({RESPONSE_DATA_KEY: jwt_token})

    def __handle_ssl_exception(self):
        error = 'SSL Fingerprint verification failed. Could not verify server.'
        Logger.info('BoTService', '__handle_ssl_exception error:' + error)
        raise falcon.HTTPServiceUnavailable(description=error)

    def __create_session(self):
        session = requests.Session()
        session.mount(API_URL, FingerprintAdapter(SSL_FINGERPRINT))
        return session
