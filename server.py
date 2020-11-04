import subprocess
import sys

from bot_python_sdk.Utils import Utils
from bot_python_sdk.configuration_service import ConfigurationService
from bot_python_sdk.store import Store
from bot_python_sdk.logger import Logger

store = Store()


# If OS is windows based, it doesn't support gunicorn so we run waitress
# TODO doesn't work with pyCharm
def get_ip():
    ip_address = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE).communicate()[0].decode('ascii').split(' ')[0]

    Logger.info('Server', "starting with configuration... IP" + ip_address)

    if Utils.is_valid(ip_address):
        Logger.info('Server', "Detected IP Address :" + ip_address)
    else:
        ip_address = '127.0.0.1'
        Logger.info('Server', "Failed in detecting valid IP Address, using loop back address: " + ip_address)

    return ip_address


def start_server():
    ip_address = get_ip()

    Logger.info('Server', "Starting Webserver at URL: http://" + ip_address + ':3001/')
    subprocess.run(['gunicorn', '-b', ip_address + ':3001', 'bot_python_sdk.api:api'])
    Logger.info('Server', 'Webserver is running')


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

start_server()
