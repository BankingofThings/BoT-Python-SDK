import os
import subprocess
import sys

from bot_python_sdk.Utils import Utils
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger

store = Store()

# If OS is windows based, it doesn't support gunicorn so we run waitress
# TODO doesn't work with pyCharm
def startWebServer():
    ip = Utils.getIpAddress()
    Logger.info('Server', "starting with configuration... IP" + ip)
    if Utils.is_valid(ip):
        Logger.info('Server', "Detected IP Address :" + ip)
    else:
        Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: 127.0.0.1")
        ip = '127.0.0.1'

    Logger.info('Server', "Starting Webserver at URL: http://" + ip + ':3001/')
    subprocess.run(['gunicorn', '-b', ip + ':3001', 'bot_python_sdk.api:api'])
    Logger.info('Server', 'Webserver is running')


if os.name == 'nt':
    ip = Utils.getIpAddress()
    Logger.info('Server', "starting with configuration... IP" + ip)

    subprocess.run(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    if not store.has_configuration():
        if len(sys.argv) != 2:
            exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"')
        elif len(sys.argv[1]) != 36:
            exit('Please enter a valid productID')
        else:
            # argv is the console input
            productID = sys.argv[1]

            Logger.info('Server', "starting with configuration. ProductID " + productID)
            ConfigurationService().initialize_configuration(productID)

            startWebServer()
    else: startWebServer()
