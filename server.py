import os
import subprocess
import sys
import re

from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger

store = Store()


# Function to validate the given IP Address
def is_valid(ip):
    regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(
                25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''

    return re.search(regex, ip)


if not store.has_configuration():
    Logger.info('Server', "checking configuration...")
    Logger.info('Server', "sys.argv[0] = " + sys.argv[0])
    Logger.info('Server', "sys.argv[1] = " + sys.argv[1])

    if len(sys.argv) <= 1:
        exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
    # argv is ProductID from console input
    ConfigurationService().initialize_configuration(sys.argv[1])


# If OS is windows based, it doesn't support gunicorn so we run waitress
if os.name == 'nt':
    subprocess.run(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    cmd = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)

    ip = cmd.communicate()[0].decode('ascii').split(' ')[0]
    if is_valid(ip):
        Logger.info('Server', "Detected IP Address :" + ip)
    else:
        Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: 127.0.0.1")
        ip = '127.0.0.1'

    Logger.info('Server', "Starting Webserver at URL: http://" + ip + ':3001/')
    subprocess.run(['gunicorn', '-b', ip + ':3001', 'bot_python_sdk.api:api'])
