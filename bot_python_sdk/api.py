import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

Logger.info('api', 'init start')
# Triggered by gunicorn
# Start Webserver and add supported endpoint resources
api = application = falcon.API()

Logger.info('api', 'init done')
# Start finn
Finn(api)
