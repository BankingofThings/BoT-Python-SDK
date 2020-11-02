import os
import subprocess
import sys
import re

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger

configuration_service = ConfigurationService()
store = Store()
LOCATION = 'Server'


# Function to validate the given IP Address
def is_valid(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

    return re.search(regex, ip)


if not store.has_configuration():
    if len(sys.argv) <= 1:
        exit('Please add your makerID to configure the SDK: "make server makerID=YOUR_MAKER_ID"')
    maker_id = sys.argv[1]  # 1 -> First argument after server.py
    configuration_service.initialize_configuration(maker_id)

# If OS is windows based, it doesn't support gunicorn so we run waitress
if os.name == 'nt':
    subprocess.run(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    cmd = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)
    ip = cmd.communicate()[0].decode('ascii').split(' ')[0]
    if is_valid(ip):
        Logger.info(LOCATION, "STErcan Detected IP Address :" + ip)
    else:
        Logger.info(LOCATION, "Failed in detecting valid IP Address, using loop back address: 127.0.0.1")
        ip = '127.0.0.1'
    Logger.info(LOCATION, "Starting Webserver at URL: http://" + ip + ':3001/')
    subprocess.run(['gunicorn', '-b', ip + ':3001', 'bot_python_sdk.api:api'])
