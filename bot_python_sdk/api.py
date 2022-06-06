import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.util.logger import Logger

###
# Used by gunicorn, api reference is used by gunicorn
# Enables curl commands.
# This file is started by gunicorn, after server has started.
##
api = application = falcon.API()

Logger.info('api', 'init done')

Finn(None, None, None, None, api)
