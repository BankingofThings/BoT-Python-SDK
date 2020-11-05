import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

api = application = falcon.API()

Logger.info('api', 'init done')

Finn.on_server_ready(api)

