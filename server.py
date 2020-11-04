import subprocess

from bot_python_sdk.Utils import Utils

# Start application
from bot_python_sdk.logger import Logger

__ip_address = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]

Logger.info('Server', "starting with configuration... IP" + __ip_address)

if Utils.is_valid(__ip_address):
    Logger.info('Server', "Detected IP Address :" + __ip_address)
else:
    __ip_address = '127.0.0.1'
    Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + __ip_address)

Logger.info('Server', "Starting server at URL: http://" + __ip_address + ':3001/')

# Executes api.py and indirectly finn.py
subprocess.run(['gunicorn', '-b', __ip_address + ':3001', 'bot_python_sdk.api:api'])
