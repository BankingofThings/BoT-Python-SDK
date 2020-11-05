import atexit
import os
import signal
import subprocess

import falcon

from bot_python_sdk.finn import Finn
from bot_python_sdk.utils import Utils

from bot_python_sdk.logger import Logger

# Start application
# 1. this file
# 2. gunicorn starts file api.py
# 3. api.py starts instance of Finn
__ip_address = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]

Logger.info('Server', "starting with configuration... IP" + __ip_address)

if Utils.is_valid(__ip_address):
    Logger.info('Server', "Detected IP Address :" + __ip_address)
else:
    __ip_address = '127.0.0.1'
    Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + __ip_address)

Logger.info('Server', "Starting server at URL: http://" + __ip_address + ':3001/')

# api = application = falcon.API()
# Finn(api)

# Executes api.py and indirectly finn.py
subprocess.run(['gunicorn', '-b', __ip_address + ':3001', 'bot_python_sdk.api:api'])
#
# def __stop_gunicorn():
#     Logger.info('Server', '__stop_gunicorn')
#     os.kill(process.pid, signal.SIGTERM)
#
#
# atexit.register(__stop_gunicorn)
