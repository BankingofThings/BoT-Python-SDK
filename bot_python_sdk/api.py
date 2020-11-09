import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

###
# Used by gunicorn, api reference is used by gunicorn
##
api = application = falcon.API()

Logger.info('api', 'init done')

Finn(None, None, None, None, api)
