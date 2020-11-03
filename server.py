import os
import subprocess
import sys

from bot_python_sdk.Utils import Utils
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger

store = Store()
c = ConfigurationService()

if not store.has_configuration():
    if len(sys.argv) != 4:
        exit('Please add your productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID"'.join(sys.argv))
    elif len(sys.argv) == 4 and len(sys.argv[4]) != 46:
        exit('Please enter a VALID productID to configure the SDK: "make server productID=YOUR_PRODUCT_ID" (' + sys.argv[1] + len(sys.argv[1]) +')')
    else:
        Logger.info('Server', "starting with configuration...")

    # argv is the console input
    ConfigurationService().initialize_configuration(sys.argv[1])

# If OS is windows based, it doesn't support gunicorn so we run waitress
if os.name == 'nt':
    subprocess.run(['waitress-serve', '--port=3001', 'bot_python_sdk.api:api'])
else:
    Logger.info("ercan", ''.join(sys.argv))
    cmd = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE)

    ip = cmd.communicate()[0].decode('ascii').split(' ')[0]
    if Utils.is_valid(ip):
        Logger.info('Server', "Detected IP Address :" + ip)
    else:
        Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: 127.0.0.1")
        ip = '127.0.0.1'

    Logger.info('Server', "Starting Webserver at URL: http://" + ip + ':3001/')
    subprocess.run(['gunicorn', '-b', ip + ':3001', 'bot_python_sdk.api:api'])
    Logger.info('Server', 'Webserver is running')
