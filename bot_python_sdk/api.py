import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.logger import Logger

Logger.info('api', 'init done')
# Start finn
Finn.get_instance().on_server_ready()
